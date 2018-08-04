from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Thread(models.Model):
	thread = models.CharField(max_length=50)


class SendMessage(models.Model):
	thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	receiver = models.IntegerField()
	message = models.TextField()
	# image = models.CharField(max_length=300)
	# url = models.CharField(max_length=300)
	send_when = models.CharField(max_length=30,default="now")
	created_at = models.DateTimeField(auto_now_add=True)
	status = models.IntegerField(default=0)
	date_time = models.DateTimeField(blank=True)
	# type = models.CharField(max_length=20, blank=True)
	# object_id = models.IntegerField(default=0)

	def __str__(self):
		return  str(self.id)

class Response(models.Model):
	thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
	message = models.ForeignKey(SendMessage, on_delete=models.CASCADE)
	sender = models.IntegerField()
	receiver = models.IntegerField()
	reply = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)
	status = models.IntegerField(default=0)

	def __str__(self):
		return str(self.message)

class Notifications(models.Model):
	title = models.CharField(max_length=100)
	message = models.TextField()

	def __str__(self):
		return str(self.title)


class UserNotification(models.Model):
	status_choice = (
		(0, 'not seen'),
		(1, 'seen')
	)
	notification = models.ForeignKey(Notifications, on_delete=models.CASCADE)
	user_to = models.IntegerField()
	user_from = models.IntegerField()
	created_at = models.DateTimeField(auto_now_add=True)
	status = models.IntegerField(choices=status_choice, default=0)
	table_name = models.CharField(max_length=100, blank=True)
	table_id = models.IntegerField(default=0)

	def __str__(self):
		return str(self.notification)

class ChatGroup(models.Model):
	title = models.CharField(max_length=100)
	adminuser = models.IntegerField()
	usercount = models.IntegerField(default=0)

	def getLastUserMsg(self):
		latestmsg = Chat.objects.filter(chatgroup=self).order_by('-id')
		if latestmsg:
			return latestmsg[0].user.first_name
		else:
			return False

	def getLastMsg(self):
		latestmsg = Chat.objects.filter(chatgroup=self).order_by('-id')
		if latestmsg:
			return latestmsg[0].message
		else:
			return False


class GroupUsers(models.Model):
	chatgroup = models.ForeignKey(ChatGroup, blank=True, null=True, on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE)

class Chat(models.Model):
	chatgroup = models.ForeignKey(ChatGroup, blank=True, null=True, on_delete=models.CASCADE)
	user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
	message = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)

class GroupRequests(models.Model):
	chatgroup = models.ForeignKey(ChatGroup, blank=True, null=True, on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
