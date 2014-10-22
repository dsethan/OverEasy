from django.conf.urls import patterns, url, include	
from django.contrib import admin
from users import views

admin.autodiscover()

urlpatterns = patterns('',
	url(r'^login', views.user_login, name='user_login'),
    url(r'^register', views.user_reg, name='user_reg'),
    url(r'^process_new_user', views.process_new_user, name='process_new_user'),
    url(r'^logout', views.user_logout, name='user_logout'),
    url(r'^homemenu', views.homemenu, name='homemenu'),
    )
