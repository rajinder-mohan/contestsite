from django.conf.urls import url
from .views import *

urlpatterns = [
	url(r'^prize-room$', PrizeHome.as_view(), name="prizeroom"),
]
