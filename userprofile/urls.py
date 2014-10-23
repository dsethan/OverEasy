from django.conf.urls import patterns, url, include	
from django.contrib import admin
from users import views

admin.autodiscover()

urlpatterns = patterns('',
	url(r'^$', views.display_profile, name='display_profile'),
    )
