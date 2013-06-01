from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = patterns('',
    url(r'^$', 'memcachier_algebra.views.home', name='home'),
    url(r'^compute/$', 'memcachier_algebra.views.compute', name='compute'),
)

urlpatterns += staticfiles_urlpatterns()
