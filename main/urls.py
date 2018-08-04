from django.conf.urls import url
from django.contrib.auth import views
from django.contrib.auth.views import logout
from .views import *

urlpatterns = [
	url(r'^$', IndexPage.as_view(), name="indexpage"),
	url(r'^login$', Login.as_view(), name="login"),
	url(r'^homepage$', Home.as_view(), name="home"),
	url(r'^register$', Register.as_view(), name="register"),
    url(r'^find-friends$', FindFriends.as_view(), name="findfriends"),
    url(r'^add-friend$', AddFriend.as_view(), name="addfriend"),
    url(r'^accept-request$', AcceptRequest.as_view(), name="acceptrequest"),
    url(r'^friend-requests$', FriendRequest.as_view(), name="friendrequests"),
	url(r'^delete-request$', DeleteReceiveRequest.as_view(), name="deleterequest"),
    url(r'^cancel-requests$', DeleteSendRequest.as_view(), name="cancelrequests"),
    url(r'^friends$', Friends.as_view(), name="friendlist"),
    url(r'^logout$', logout, name='logout'),
	url(r'^edit-profile$', EditProfile.as_view(), name="editprofile"),
	url(r'^chatpage$', ChatPage.as_view(), name="chatpage"),
	url(r'^faq$', Faq.as_view(), name="faq"),
	url(r'^contactus$', ContactUsView.as_view(), name="contactus"),
]
