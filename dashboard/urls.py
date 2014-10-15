from django.conf.urls import patterns, url, include	
from django.contrib import admin
from dashboard import views

admin.autodiscover()

urlpatterns = patterns('',
	url(r'^set_calendar', views.set_calendar, name='set_calendar'),
	url(r'^set_menu', views.set_menu, name='set_menu'),
	url(r'^initialize_new_menu_item', views.initialize_new_menu_item, name='initialize_new_menu_item'),
	url(r'^cal_process_add', views.cal_process_add, name='cal_process_add'),
	url(r'^initialize_week', views.initialize_week, name='initialize_week'),
    )
