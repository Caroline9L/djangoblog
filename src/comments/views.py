from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect, Http404, HttpResponse 
from django.shortcuts import render, get_object_or_404

from .forms import CommentForm
from .models import Comment

@login_required #(login_url="/login/") #will redirect if commenter is not logged in. ditched the param since it got added in settings. Can override that to a different login screen or whatever from here same way
def comment_delete(request, id):
	# obj = get_object_or_404(Comment, id=id)
	try: 
		obj = Comment.objects.get(id=id)
	except:
		raise Http404

	if obj.user != request.user:
		# messages.success(request, "User does not have permission to complete action.")
		# raise Http404
		response = HttpResponse("User does not have permission to complete action.")
		response.status_code = 403 # permissions status code
		return response
		# return render(request, "confirm_delete.html", context, status_code=403)
	
	if request.method == "POST": #requires blank form submission to complete request
		parent_obj_url = obj.content_object.get_absolute_url()
		obj.delete()
		messages.success(request, "This has been deleted")
		return HttpResponseRedirect(parent_obj_url)
	context = {
		"object": obj,
	}
	return render(request, "confirm_delete.html", context)

def comment_thread(request, id):
	# obj = get_object_or_404(Comment, id=id)
	try: 
		obj = Comment.objects.get(id=id)
	except:
		raise Http404

	if not obj.is_parent:
		obj = obj.parent #reset original var to parent obj

	content_object = obj.content_object #parent post
	content_id = obj.content_object.id

	initial_data = {
		"content_type": obj.content_type, 
		"object_id": obj.object_id,
		# "parent_obj": None
	}
	form = CommentForm(request.POST or None, initial=initial_data)
	if form.is_valid() and request.user.is_authenticated():
		c_type = form.cleaned_data.get("content_type")
		content_type = ContentType.objects.get(model=c_type)
		obj_id = form.cleaned_data.get('object_id')
		content_data = form.cleaned_data.get("content")
		#parent object
		parent_obj = None
		try:
			parent_id = int(request.POST.get("parent_id"))
		except:
			parent_id = None

		if parent_id:
			parent_qs = Comment.objects.filter(id=parent_id)
			if parent_qs.exists() and parent_qs.count() == 1:
				parent_obj = parent_qs.first()

		new_comment, created = Comment.objects.get_or_create(
			user = request.user,
			content_type = content_type, 
			object_id = obj_id,
			content = content_data,
			parent = parent_obj,
		)
		return HttpResponseRedirect(new_comment.content_object.get_absolute_url())
		
	context = {
		"comment": obj,
		"form": form,
	}
	return render(request, "comment_thread.html", context)


# def post_detail(request, slug):
# 	instance = get_object_or_404(Post, slug=slug)
# 	if instance.draft or instance.publish > timezone.now().date():
# 		if not request.user.is_staff or not request.user.is_superuser:
# 			raise Http404
# 	share_string = quote_plus(instance.content)

# 	#comments
# 	initial_data = {
# 		"content_type": instance.get_content_type, 
# 		"object_id": instance.id,
# 	}

	comments = instance.comments

	context = {
        "title": instance.title,
		"instance": instance,
		"share_string": share_string,
		"comments": comments,
		"comment_form": form,
    }
	return render(request, "post_detail.html", context)
