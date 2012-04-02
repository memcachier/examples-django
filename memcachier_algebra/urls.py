from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'memcachier_algebra.views.home', name='home'),
    url(r'^compute/', 'memcachier_algebra.views.compute', name='compute'),
)
