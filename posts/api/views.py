from django.db.models import Q
from rest_framework.filters import (
	SearchFilter,
	OrderingFilter,
	)
from rest_framework.generics import (
	CreateAPIView,
	DestroyAPIView,
	ListAPIView, 
	UpdateAPIView,
	RetrieveAPIView, 
	RetrieveUpdateAPIView,
	)
# from rest_framework.pagination import (
# 	LimitOffsetPagination,
# 	PageNumberPagination,
# 	)
from rest_framework.permissions import (
	AllowAny,
	IsAuthenticated,
	IsAdminUser,
	IsAuthenticatedOrReadOnly,
)

from posts.models import Post
from .pagination import PostLimitOffsetPagination, PostPageNumberPagination
from .permissions import IsOwnerOrReadOnly
from .serializers import (
	PostCreateUpdateSerializer, 
	PostDetailSerializer,
	PostListSerializer
	)

class PostCreateAPIView(CreateAPIView):
	queryset = Post.objects.all()
	serializer_class = PostCreateUpdateSerializer
	# permission_classes = [IsAuthenticated]

	def perform_create(self, serializer):
		serializer.save(user=self.request.user) #self.request is class-based way to get request, rather than just passing request as a param

class PostDetailAPIView(RetrieveAPIView):
	queryset = Post.objects.all()
	serializer_class = PostDetailSerializer
	lookup_field = 'slug'
	permission_classes = [AllowAny]

class PostUpdateAPIView(RetrieveUpdateAPIView): #this view will prepopulate fields and display data to edit
	queryset = Post.objects.all()
	serializer_class = PostCreateUpdateSerializer
	lookup_field = 'slug'
	# permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
	permission_classes = [IsOwnerOrReadOnly]

	def perform_update(self, serializer):
		serializer.save(user=self.request.user)

	

class PostDeleteAPIView(DestroyAPIView):
	queryset = Post.objects.all()
	serializer_class = PostDetailSerializer
	lookup_field = 'slug'
	permission_classes = [IsOwnerOrReadOnly]

class PostListAPIView(ListAPIView):
	# queryset = Post.objects.all()
	serializer_class = PostListSerializer
	permission_classes = [AllowAny]
	filter_backends = [SearchFilter, OrderingFilter] #similar to list filter in admin
	search_fields = ['title', 'content', 'user__first_name'] #similar to admin
	# pagination_class = LimitOffsetPagination  #limit is # to return, offset starts results after #(?)
	# pagination_class = PostLimitOffsetPagination
	pagination_class = PostPageNumberPagination

	def get_queryset(self, *args, **kwargs):
		queryset_list = Post.objects.all() #our default, or class default: super(PostListAPIView, self).get_queryset(*args, **kwargs)
			#Post.objects.filter() can add filters, ie (user=self.request.user)
		query = self.request.GET.get("q") #add self cause it's class-based!
		if query:
			queryset_list = queryset_list.filter(
				Q(title__icontains=query) |
				Q(content__icontains=query) |
				Q(user__first_name__icontains=query) |
				Q(user__last_name__icontains=query)
				).distinct()
		return queryset_list
