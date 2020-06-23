from django.conf.urls import url
from scanner_api import views
from django.urls import include, path

urlpatterns = [
    path('', views.ScanView.as_view(), name='scan_view'),
]