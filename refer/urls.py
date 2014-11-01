from django.conf.urls import patterns, url, include	
from django.contrib import admin
from refer import views

admin.autodiscover()

urlpatterns = patterns('',
	url(r'^process_referral', views.process_referral, name='process_referral'),
    )
