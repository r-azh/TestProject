from django.conf.urls import include, url
from django.contrib import admin

__author__ = 'R.Azh'

from . import views

urlpatterns = [
    url(r'^polls/$', views.PollList.as_view()),
    url(r'polls/(?P<pk>[0-9]+)/$', views.PollDetail.as_view()),
    url(r'^create_user/$', views.UserCreate.as_view()),
    url(r'^choices/(?P<pk>[0-9]+)/$', views.ChoiceDetail.as_view()),
    url(r'^create_vote/$', views.CreateVote.as_view()),
    url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),
]