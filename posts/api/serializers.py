# from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from posts.models import Post


class PostCreateUpdateSerializer(ModelSerializer):
	class Meta:
		model = Post
		fields = [
			"title",
			"content",
			"publish"
		]


class PostDetailSerializer(ModelSerializer):
	class Meta:
		model = Post
		fields = [
			"id",
			"title",
			"slug",
			"content",
			"publish"
		]

class PostListSerializer(ModelSerializer):
	class Meta:
		model = Post
		fields = [
			"title",
			"slug",
			"content",
			"publish"
		]



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