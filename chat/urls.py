from django.conf.urls import url
from .views import *

urlpatterns = [
	url(r'^signals', signal_notification),
	url(r'^send', send_message),
	url(r'^team$', Team.as_view(), name="team"),
	url(r'^chatbox$', ChatboxMessages.as_view(), name="chatbox"),
]
