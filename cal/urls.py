from django.conf.urls import patterns, url, include	
from django.contrib import admin
from cal import views

admin.autodiscover()

urlpatterns = patterns('',
	url(r'^$', views.render_first_look_calendar, name='render_first_look_calendar'),
    )
