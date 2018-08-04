from django.conf.urls import url
from .views import *

urlpatterns = [
	url(r'^bridge$', TheBridge.as_view(), name="bridge"),
]
