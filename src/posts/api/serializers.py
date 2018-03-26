# from rest_framework import serializers
from rest_framework.serializers import (
	HyperlinkedIdentityField, 
	ModelSerializer, 
	SerializerMethodField
	)

from comments.api.serializers import CommentSerializer
from comments.models import Comment
from posts.models import Post


class PostCreateUpdateSerializer(ModelSerializer):
	class Meta:
		model = Post
		fields = [
			"title",
			"content",
			"publish"
		]

#Can globally declare the hyperlink...
post_detail_url = HyperlinkedIdentityField(
		view_name='posts-api:detail',
		lookup_field='slug'
		)

class PostDetailSerializer(ModelSerializer):
	url = post_detail_url #...and call it like this
	user = SerializerMethodField()
	image = SerializerMethodField()
	html = SerializerMethodField()
	comments = SerializerMethodField()
	class Meta:
		model = Post
		fields = [
			"url",
			"id",
			"user",
			"title",
			"slug",
			"content",
			"html",
			"publish",
			"image",
			"comments"
		]

	def get_html(self, obj):
		return obj.get_markdown()

	def get_user(self, obj): #declare get_ + var
		return str(obj.user.username)

	def get_image(self, obj):
		try: 
			image = obj.image.url
		except:
			image = None
		return image

	def get_comments(self, obj):
		# content_type = obj.get_content_type #as defined in models.py
		# object_id = obj.id
		c_qs = Comment.objects.filter_by_instance(obj) #as defined in comment class, models.py, covers above args
		comments = CommentSerializer(c_qs, many=True).data
		return comments



class PostListSerializer(ModelSerializer):
	# url = HyperlinkedIdentityField( #gives link to the detail info json
	# 	view_name='posts-api:detail', #namespace in url setup + name in api url setup
	# 	lookup_field='slug' #default pk, or what we are using to identify the detail 
	# 	)
	# delete_url = HyperlinkedIdentityField(
	# 	view_name='posts-api:delete',
	# 	lookup_field='slug'
	# 	)
	url = post_detail_url
	user = SerializerMethodField()
	class Meta:
		model = Post
		fields = [
			"url",
			"user",
			"title",
			# "slug",
			"content",
			"publish",
			# "delete_url"
		]

	def get_user(self, obj): #declare get_ + var
		return str(obj.user.username)


"""

data = {
	"title": "A title",
	"content": "Some content",
	"publish": "2018-03-22",
	"slug": "A-title",
}

new_item = PostSerializer(data=data)
if new_item.is_valid():
	new_item.save()
else:
	print(new_item.errors)

"""