from django.conf.urls import patterns, url, include	
from django.contrib import admin
from driver import views

admin.autodiscover()

urlpatterns = patterns('',
	url(r'^$', views.view_driver, name='view_driver'),
    )
