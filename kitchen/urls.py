from django.conf.urls import patterns, url, include	
from django.contrib import admin
from kitchen import views

admin.autodiscover()

urlpatterns = patterns('',
	url(r'^$', views.view_kitchen, name='view_kitchen'),
    )
