from django.conf.urls import patterns, url, include	
from django.contrib import admin
from home import views

admin.autodiscover()

urlpatterns = patterns('',
	url(r'^$', views.home, name='home'),
    )
