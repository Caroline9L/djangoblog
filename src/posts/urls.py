from django.conf.urls import url
from django.contrib import admin

from .views import (
	post_list,
	post_create,
	post_update,
	post_detail,
	post_delete,
)

urlpatterns = [
    url(r'^$', post_list, name="list"), #blank makes it default home page
    url(r'^create/$', post_create),
    url(r'^(?P<slug>[\w-]+)/$', post_detail, name="detail"),
	url(r'^(?P<slug>[\w-]+)/edit/$', post_update, name='update'),
    url(r'^(?P<slug>[\w-]+)/delete/$', post_delete),
]
