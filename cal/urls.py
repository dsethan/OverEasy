from django.conf.urls import patterns, url, include	
from django.contrib import admin
from cal import views

admin.autodiscover()

urlpatterns = patterns('',
	url(r'^$', views.render_first_look_calendar, name='render_first_look_calendar'),
	url(r'^entry_not_avail/', views.render_second_look_calendar, name='render_second_look_calendar'),
	url(r'^(?P<entry_id>\d+)/$', views.process_cal, name='process_cal'),

    )
