from django.conf.urls import patterns, url, include	
from django.contrib import admin
from menu import views

admin.autodiscover()

urlpatterns = patterns('',
	url(r'^$', views.display_menu, name='display_menu'),
    )