from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', include('users.urls')),
    url(r'^cal/', include('cal.urls')),
    url(r'^menu/', include('menu.urls')),
    url(r'^dashboard/', include('dashboard.urls')),
    url(r'^checkout/', include('checkout.urls')),
)
