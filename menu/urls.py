from django.conf.urls import patterns, url, include	
from django.contrib import admin
from menu import views

admin.autodiscover()

urlpatterns = patterns('',
	url(r'^$', views.add_item_to_cart, name='add_item_to_cart'),
	url(r'^display_menu/', views.display_menu, name='display_menu'),
	url(r'^remove_from_cart/', views.remove_from_cart, name='remove_from_cart'),

    )
