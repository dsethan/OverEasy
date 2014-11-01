from django.conf.urls import patterns, url, include	
from django.contrib import admin
from userprofile import views

admin.autodiscover()

urlpatterns = patterns('',
	url(r'^$', views.display_profile, name='display_profile'),
	url(r'^process_phone_number', views.process_phone_number, name="process_phone_number"),
    )
