from django.conf.urls import patterns, url, include	
from django.contrib import admin
from drivers import views

admin.autodiscover()

urlpatterns = patterns('',
	url(r'^$', views.view_driver, name='view_driver'),
	url(r'^manage_drivers', views.manage_drivers, name='manage_drivers'),
	url(r'^process_arrival', views.process_arrival, name='process_arrival'),

    )
