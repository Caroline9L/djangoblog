from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import pre_save
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.utils.text import slugify

from markdown_deux import markdown
from comments.models import Comment

from .utils import get_read_time
# Create your models here.

class PostManager(models.Manager):
	def active(self, *args, **kwargs):
		# Post.objects.all() = super(PostManager, self).all()
		return super(PostManager, self).filter(draft=False).filter(publish__lte=timezone.now())

def upload_location(instance, filename):
	# filebase, extension = filename.split(".")
	# return "%s/%s.%s" % (instance.id, instance.id, filename)
# renames file name as post id, kind of breakable
	return "%s/%s" %(instance.id, filename)

class Post(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
	title = models.CharField(max_length=120)
	slug = models.SlugField(unique=True)
	# image = models.FileField(null=True, blank=True)
	image = models.ImageField(upload_to=upload_location,
		null=True, 
		blank=True, 
		height_field="height_field", 
		width_field="width_field")
	height_field = models.IntegerField(default=0)
	width_field = models.IntegerField(default=0)
	content = models.TextField()
	draft = models.BooleanField(default=False)
	publish = models.DateField(auto_now=False, auto_now_add=False)
	# read_time = models.TimeField(null=True, blank=True)
	read_time = models.IntegerField(default=0)
	updated = models.DateTimeField(auto_now=True, auto_now_add=False)
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

	objects = PostManager() #filters out drafts, links in new class


	def __unicode__(self):
		return self.title

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse("posts:detail", kwargs={"slug": self.slug})
		# return "/posts/%s/" %(self.id)

	class Meta:
		ordering = ["-id", "-timestamp", "-updated"]

	def get_markdown(self):
		content = self.content
		markdown_text = markdown(content)
		return mark_safe(markdown_text)

	@property
	def comments(self):
		instance = self
		qs = Comment.objects.filter_by_instance(self)
		return qs

	@property
	def get_content_type(self):
		instance = self
		content_type = ContentType.objects.get_for_model(instance.__class__)
		return content_type



def create_slug(instance, new_slug=None):
	slug = slugify(instance.title)
	if new_slug is not None:
		slug = new_slug
	qs = Post.objects.filter(slug=slug).order_by("-id")
	exists = qs.exists()
	if exists:
		new_slug = "%s-%s" %(slug, qs.first().id)
		return create_slug(instance, new_slug=new_slug)
	return slug


def pre_save_post_receiver(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = create_slug(instance)

	if instance.content:
		html_string = instance.get_markdown()
		read_time_var = get_read_time(html_string)
		instance.read_time = read_time_var


	# slug = slugify(instance.title)
	# exists = Post.objects.filter(slug=slug).exists()
	# if exists:
	# 	slug = "%s-%s" %(slug, instance.id)
	# instance.slug = slug

pre_save.connect(pre_save_post_receiver, sender=Post)
