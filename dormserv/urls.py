from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^users/', include('users.urls')),
    url(r'^cal/', include('cal.urls')),
    url(r'^menu/', include('menu.urls')),
    url(r'^dashboard/', include('dashboard.urls')),
    url(r'^checkout/', include('checkout.urls')),
)

if not settings.DEBUG:
   urlpatterns += patterns('',
       (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
   )