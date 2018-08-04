from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from main.models import *
from django.conf import settings
from datetime import datetime
from django.contrib.auth.models import User
from django.views.generic import TemplateView, View
from django.db.models import Q
import time
import json


class Team(TemplateView):
	template_name = 'team.html'
	def get(self, request, *args, **kwargs):

		user = User.objects.get(id=request.user.id)
		profile = Profile.objects.get(user=request.user)
		exclude_users = []
		if profile.friends:
			exclude_users = json.loads(profile.friends)
		exclude_users.append(request.user.id)
		try:
			incoming = FriendRequests.objects.get(user=request.user)
			requestlist1 = json.loads(incoming.newrequests)
			exclude_users = exclude_users + requestlist1
		except Exception as e:
			pass
		try:
			outgoing = SendRequests.objects.get(user=request.user)
			requestlist2 = json.loads(outgoing.newrequests)
			exclude_users = exclude_users + requestlist2
		except Exception as e:
			pass
		findfriendslist = User.objects.filter(is_staff=0, is_superuser=0).exclude(id__in=exclude_users)
		users1=[]
		users2=[]
		try:
			incoming = FriendRequests.objects.get(user=request.user)
			requestlist1 = json.loads(incoming.newrequests)
			receivefriendrequets = User.objects.filter(id__in=requestlist1)
		except Exception as e:
			pass
		try:
			outgoing = SendRequests.objects.get(user=request.user)
			requestlist2 = json.loads(outgoing.newrequests)
			sendfriendrequets = User.objects.filter(id__in=requestlist2)
		except Exception as e:
			pass
		fiendslist=[]
		profile = Profile.objects.get(user=request.user)
		if profile.friends:
			fiendslist = json.loads(profile.friends)
		allfriends = User.objects.filter(id__in=fiendslist)

		threadlist = []
		sendmessage = SendMessage.objects.filter(Q(user__id=request.user.id)|Q(receiver=request.user.id))
		for msg in sendmessage:
			messageslist = {}
			messagesquery = Response.objects.filter(thread__id=msg.thread.id).order_by('-id')
			if messagesquery:
				if messagesquery[0].sender==request.user.id:
					messageslist["sender"]="Me :"
					user = User.objects.get(id=messagesquery[0].receiver)
					messageslist["name"] = (user.first_name).title()+" "+(user.last_name).title()
					messageslist["msg"] = messagesquery[0].reply
					messageslist["date"] = messagesquery[0].created_at
					messageslist["userid"] = user.id
				else:
					messageslist["sender"] = ""
					user = User.objects.get(id=messagesquery[0].sender)
					messageslist["name"] = (user.first_name).title()+" "+(user.last_name).title()
					messageslist["msg"] = messagesquery[0].reply
					messageslist["date"] = messagesquery[0].created_at
					messageslist["userid"] = user.id
			else:
				if msg.user.id==request.user.id:
					messageslist["sender"]="Me :"
					user = User.objects.get(id=msg.receiver)
					messageslist["name"] = (user.first_name).title()+" "+(user.last_name).title()
					messageslist["msg"] = msg.message
					messageslist["date"] = msg.created_at
					messageslist["userid"] = user.id
				else:
					messageslist["sender"] = ""
					user = User.objects.get(id=msg.user.id)
					messageslist["name"] = (user.first_name).title()+" "+(user.last_name).title()
					messageslist["msg"] = msg.message
					messageslist["date"] = msg.created_at
					messageslist["userid"] = user.id
			threadlist.append(messageslist)
		return render(request, self.template_name,locals())

class ChatboxMessages(View):
	def get(self, request):
		user_id = request.user.id
		receiver_id = request.GET.get("id")
		response = {}
		messagelist = []
		msgdict = {}
		msg = ""
		response_msgs = ""
		try:
			msg = SendMessage.objects.get(user__id=user_id,receiver=int(receiver_id))
			msgdict["me"] ="sender"
			msgdict["msg"] = msg.message
			messagelist.append(msgdict)
			response_msgs = Response.objects.filter(thread=msg.thread).order_by('id')
			if response_msgs:
				for msgs in response_msgs:
					msgdict = {}
					if msgs.sender==request.user.id:
						msgdict["me"] ="sender"
						msgdict["msg"] = msgs.reply
					else:
						msgdict["me"] ="receiver"
						msgdict["msg"] = msgs.reply
					messagelist.append(msgdict)

		except SendMessage.DoesNotExist:
			try:
				msg = SendMessage.object.get(user__id=int(receiver_id),receiver=user_id)
				msgdict["me"] ="sender"
				msgdict["msg"] = msg.message
				messagelist.append(msgdict)
				response_msgs = Response.objects.filter(thread=msg.thread).order_by('id')
				if response_msgs:
					for msgs in response_msgs:
						msgdict = {}
						if msgs.sender==request.user.id:
							msgdict["me"] ="sender"
							msgdict["msg"] = msgs.reply
						else:
							msgdict["me"] ="receiver"
							msgdict["msg"] = msgs.reply
						messagelist.append(msgdict)
			except Exception as e:
				pass

		response["data"] = "available"
		response["msg"] = messagelist
		return HttpResponse(json.dumps(response))

def notifications(request, user_id):
	user_to = user_id
	notification_list = []

	notifications = UserNotification.objects.filter(user_to=user_to, status=0)

	for notification in notifications:
		status = notification.status

		if status == 0:
			id = notification.id

			user_from = notification.user_from

			notification_id = notification.notification_id

			table_name = notification.table_name

			table_id = notification.table_id

			if table_name != "chat":
				notification_detail = Notifications.objects.get(id=notification_id)
				title = notification_detail.title
				message = notification_detail.message
				notification_list.append({'id': id, 'user_from': user_from, 'status': status, 'title': title, 'message': message})
	return HttpResponse(json.dumps(notification_list))


def signal_notification(request):
	user_id = request.user.id
	receiver_id = request.GET.get("receiver_id")
	msg = ""
	response_msgs = ""
	try:
		msg = SendMessage.objects.get(user__id=user_id,receiver=receiver_id)
		response_msgs = Response.objects.filter(thread=msg.thread).order_by('-id')[0]
	except SendMessage.DoesNotExist:
		try:
			msg = SendMessage.object.get(user__id=receiver_id,receiver=user_id)
			response_msgs = Response.objects.filter(thread=msg.thread).order_by('-id')[0]
		except Exception as e:
			pass
	response = {}
	if response_msgs:
		response["data"] = "available"
		response["msg"] = response_msgs.reply
		if user_id == response_msgs.sender:
			response["status"] = "send"
		else:
			response["status"] = "received"
	else:
		response["data"] = "unavailable"

	return HttpResponse(json.dumps(response))

def send_message(request):
	response = {}
	user_id = request.user.id
	msg = request.GET.get("msg")
	receiver_id = request.GET.get("receiver_id")
	try:
		send_msg = SendMessage.objects.get(user__id=user_id,receiver=int(receiver_id))
		response_msg = Response(thread=send_msg.thread,message=send_msg,sender=user_id,receiver=int(receiver_id),reply=msg)
		response_msg.save()
		response["status"] = "status"
	except SendMessage.DoesNotExist:
		date_time = datetime.now()
		thread = str(int(time.time()))+str(user_id)
		record = Thread(thread=thread)
		record.save()
		thread_id = record.id
		send_msg = SendMessage(user_id=user_id,receiver=int(receiver_id),message=msg,thread_id=thread_id,date_time=date_time)
		send_msg.save()
	except Exception as e:
		raise
		# print(e)
		# response["status"] = "fail"
	return HttpResponse(json.dumps(response))
