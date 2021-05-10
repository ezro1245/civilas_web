from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
    path('add_report', views.add_report, name='add_report')
]