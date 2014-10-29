from django.conf.urls import patterns, url, include	
from django.contrib import admin
from checkout import views

admin.autodiscover()

urlpatterns = patterns('',
	url(r'^$', views.checkout, name='checkout'),
	url(r'^process_new_card/', views.process_new_card, name='process_new_card'),
	url(r'^process_existing_card/', views.process_existing_card, name='process_existing_card'),
	url(r'^oatmeal_day_special/', views.oatmeal_day_special, name='oatmeal_day_special'),

    )


