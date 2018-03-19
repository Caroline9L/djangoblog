from urllib.parse import quote_plus

from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

# Create your views here.
from .forms import PostForm
from .models import Post

# def posts_home(request):
# 	return HttpResponse("<h1>Hello</h1>")

def post_create(request):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	form = PostForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		instance = form.save(commit=False)
		print(form.cleaned_data.get("title"))
		instance.save()
		messages.success(request, "Successfully created!")
		return HttpResponseRedirect(instance.get_absolute_url())
	# else: 
	# 	messages.error(request, "Oh no, something went wrong!")
	# if request.method == "POST":
	# 	print(request.POST.get("content"))
	# 	print(request.POST.get("title"))
	context = {
		"form": form,
	}
	return render(request, "post_form.html", context)
	# return HttpResponse("<h1>Create</h1>")

def post_detail(request, slug):
	# return HttpResponse("<h1>Detail</h1>")
	# instance = Post.objects.get(id=2)
	instance = get_object_or_404(Post, slug=slug)
	if instance.draft or instance.publish > timezone.now().date():
		if not request.user.is_staff or not request.user.is_superuser:
			raise Http404
	share_string = quote_plus(instance.content)
	context = {
        "title": instance.title,
		"instance": instance,
		"share_string": share_string,
    }
	return render(request, "post_detail.html", context)

def post_list(request):
	today = timezone.now().date()
	queryset_list = Post.objects.active()
	if request.user.is_staff or request.user.is_superuser:
		queryset_list = Post.objects.all()
	# queryset_list = Post.objects.all() # .order_by("-timestamp")
	# queryset_list = Post.objects.filter(draft=False).filter(publish__lte=timezone.now())

	#search
	query = request.GET.get("query")
	if query:
		queryset_list = queryset_list.filter(
			Q(title__icontains=query) |
			Q(content__icontains=query) |
			Q(user__first_name__icontains=query) |
			Q(user__last_name__icontains=query)
			).distinct()

	#pagination
	paginator = Paginator(queryset_list, 10)
	page_request_variable = "page"
	page = request.GET.get(page_request_variable)
	# page = request.GET.get('page')
	try:
		queryset = paginator.page(page)
	except PageNotAnInteger:
		queryset = paginator.page(1)
	except EmptyPage:
		queryset = paginator.page(paginator.num_pages)

	context = {
		"object_list": queryset,
        "title": "List",
		"page_request_variable": page_request_variable,
		"today": today, 
    }
	return render(request, "post_list.html", context)
	# return HttpResponse("<h1>List</h1>")
	# if request.user.is_authenticated():
	# 	context = {
	# 		"title": "My User List"
	# 	}
	# else: 
	# 	context = {
    #         "title": "List"
    #     }

def post_update(request, slug=None):
	# return HttpResponse("<h1>Update</h1>")
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404

	# if not request.user.is_authenticated():
	# 	raise Http404

	instance = get_object_or_404(Post, slug=slug)
	form = PostForm(request.POST or None, request.FILES or None, instance=instance)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.user = request.user
		instance.save()
		# messages.success(request, "<a href='#'>Successfully updated!</a>", extra_tags='html_safe')
		messages.success(request, "Successfully updated!")
		return HttpResponseRedirect(instance.get_absolute_url())
	context = {
            "title": instance.title,
            "instance": instance,
			"form": form,
        }
	return render(request, "post_form.html", context)

def post_delete(request, slug=None):
	# return HttpResponse("<h1>Delete</h1>")
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	instance = get_object_or_404(Post, slug=slug)
	instance.delete()
	messages.success(request, "Successfully deleted!")
	return redirect("posts:list")



# from django.shortcuts import render

# def listing(request):
#     contact_list = Contacts.objects.all()
#     paginator = Paginator(contact_list, 25) # Show 25 contacts per page

#     page = request.GET.get('page')
#     contacts = paginator.get_page(page)
#     return render(request, 'list.html', {'contacts': contacts})
