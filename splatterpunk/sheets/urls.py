from django.conf.urls import patterns, url
from django.contrib import admin

from . import views

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', views.SheetView.as_view(), name='root'),
)
