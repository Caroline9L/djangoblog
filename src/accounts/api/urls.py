from django.conf.urls import url
from django.contrib import admin

from .views import (
	UserCreateAPIView,
	UserLoginAPIView,
	)

urlpatterns = [
	url(r'^login/$', UserLoginAPIView.as_view(), name='login'),
	url(r'^register/$', UserCreateAPIView.as_view(), name='register'),
	# url(r'^(?P<pk>\d+)/$', CommentDetailAPIView.as_view(), name='thread'),
	# url(r'^(?P<pk>\d+)/edit/$', CommentEditAPIView.as_view(), name='edit'),
]
