from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from memcachier_algebra import views

urlpatterns = patterns('',
    url(r'^compute$', views.compute),
    url(r'^$', views.home),
)

urlpatterns += staticfiles_urlpatterns()
