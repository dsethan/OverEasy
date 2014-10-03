from django.conf.urls import patterns, url
from users import views

urlpatterns = patterns('',
    url(r'^register', views.user_reg, name='user_reg'),
    url(r'^process_new_user', views.process_new_user, name='process_new_user'),
    )
