from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from socketIO_client import SocketIO
from urllib.parse import urlparse
from django.conf import settings
from django.contrib.auth.models import User
from main.models import Profile
from .models import *

parsedurl = urlparse(settings.NODEJS_SOCKET_URL)


baseurl = "%s://%s" % (parsedurl.scheme, parsedurl.hostname)
baseport = parsedurl.port if parsedurl.port != None else 80


@receiver(post_save, sender=SendMessage)
@receiver(post_save, sender=Response)
@receiver(post_save, sender=UserNotification)
@receiver(post_save, sender=Chat)

def model_post_save(sender, **kwargs):
	data = kwargs['instance']

	class_name = type(data).__name__

	chat_messages = {}

	messages = []

	notification_list = []
	events_list = []

	event_receivers = []

	users_list = []

	receivers_list = []
	if class_name == "SendMessage" or class_name == "Response":

		receiver = data.receiver

		msgs = SendMessage.objects.filter(receiver=receiver, status=0, send_when="now")
		for msg in msgs:
			id = msg.id
			sender = msg.user_id
			message = msg.message
			thread_id = msg.thread_id

			date_time = msg.date_time
			date = "%s-%s-%s" % (date_time.year, date_time.month, date_time.day)
			time = date_time.strftime("%-I:%M%P")
			#sender detail
			sender_detail = User.objects.get(id=sender)
			first_name = sender_detail.first_name
			last_name = sender_detail.last_name
			name = first_name + " " + last_name
			sender_name = name.title()

			message_link = ''

			#profile
			picture = ''
			folder = ''
			src = ''
			profile = Profile.objects.filter(user_id=sender)
			if profile:
				image = profile[0].image
				if image:
					src = image.url

			messages.append({'msg_id': id, 'sender_name': sender_name, 'src': src, 'date': date, 'time': time, 'message': message, 'message_link': message_link, 'receiver': receiver})
			receivers_list.append(receiver)

		responses = Response.objects.filter(receiver=receiver, status=0)
		for response in responses:
			message_id = response.message_id
			message = response.reply
			sender = response.sender

			sender_detail = User.objects.get(id=sender)
			firstname = sender_detail.first_name
			lastname = sender_detail.last_name
			sender_name = firstname + " " + lastname
			sender_name = sender_name.title()

			thread_id = response.thread_id

			src = ''

			basic_detail = Profile.objects.filter(user_id=sender)
			if basic_detail:
				image = basic_detail[0].image
				if image:
					src = image.url

			date_time = response.created_at

			date = "%s-%s-%s" % (date_time.day, date_time.month, date_time.year)
			time = date_time.strftime("%-I:%M%P")

			message_link = "/messages/view/thread/" + str(thread_id)

			messages.append({'msg_id': message_id, 'sender_name': sender_name, 'src': src, 'date': date, 'time': time, 'message': message, 'message_link': message_link, 'receiver': receiver})
			receivers_list.append(receiver)
	if class_name == "UserNotification":

		id = data.id
		user_from = data.user_from
		user_to = data.user_to
		notifications = UserNotification.objects.filter(user_to=user_to, status=0)
		for notification in notifications:
			id = notification.id
			userfrom = notification.user_from
			userto = notification.user_to
			notification_id = notification.notification_id

			table_name = notification.table_name

			notification_detail = Notifications.objects.get(id=notification_id)

			title = notification_detail.title

			message = notification_detail.message


			table_id = notification.table_id



			if table_name == "chat":

				chat_detail = Chat.objects.get(id=table_id)
				message = chat_detail.message
				sender = chat_detail.person_id

				date = chat_detail.created_at
				day = date.day
				month = date.month
				year = date.year
				date = "%s-%s-%s" % (day, month, year)

				redirect_link = ''

				redirect_link = "/events/others/view/"+str(event_id)

				events_list.append({'id': id, 'title': title, 'event_id': event_id, 'event_title': message, 'date': date, 'link': link, 'redirect_link': redirect_link, 'receiver': userto})
				event_receivers.append(userto)

	if class_name == "Chat":
		person_id = data.user_id

		message = data.message

		created_at = data.created_at

		time = created_at.strftime("%-I:%M%P")

		message_type = data.message_type

		# user detail
		user = User.objects.get(id=person_id)
		first_name = user.first_name
		last_name = user.last_name
		name = first_name + " " + last_name
		person_name = name.title()

		image_link = ''

		# person image
		profile = Profile.objects.filter(user_id=person_id)
		if profile:
			image = profile[0].image
			if image:
				image_link = image.url

		chat_messages = {'message':message,'person_id':person_id, 'person_name': person_name, 'image_link': image_link, 'message_type': message_type, 'time': time}

	with SocketIO(baseurl, baseport) as socketIO:
			socketIO.emit('admindailyspecials', {"messages_list":messages, "messages": chat_messages, "notifications": notification_list, "events_list": events_list, 'users_list': users_list, 'receivers_list': receivers_list, 'event_receivers': event_receivers, 'class_name': class_name})
