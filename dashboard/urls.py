from django.conf.urls import patterns, url, include	
from django.contrib import admin
from dashboard import views

admin.autodiscover()

urlpatterns = patterns('',
	url(r'^set_calendar', views.set_calendar, name='set_calendar'),
    )
