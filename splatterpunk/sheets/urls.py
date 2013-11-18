from django.conf.urls import patterns, url
from django.contrib import admin

from . import views

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', views.SheetListView.as_view(), name='root'),
    url(r'^(?P<pk>\w+)/$', views.SheetInstanceView.as_view(), name='root'),
)
