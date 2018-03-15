from django.contrib import admin

# Register your models here.
from .models import Post
# from posts.models import Post

class PostModelAdmin(admin.ModelAdmin):
	
	list_display = ["title", "updated", "timestamp"] # can use "__unicode__"  rather than "title"
	list_display_links = ["updated"]
	list_editable = ["title"]
	list_filter = ["updated", "timestamp"]
	search_fields = ["title", "content"]
	class Meta:
		model = Post

admin.site.register(Post, PostModelAdmin)
