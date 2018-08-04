from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
	image = models.FileField(blank=True, null=True)
	user = models.OneToOneField(User, unique=True, blank=True, null=True, verbose_name='User', on_delete=models.CASCADE)
	phone = models.CharField(max_length=50, blank=False, null=True, verbose_name='Phone Number')
	friends = models.TextField(blank=True,null=True)
	address = models.TextField(blank=True,null=True)
	age = models.IntegerField(blank=False, null=True, default=0)
	chracter = models.CharField(max_length=50, blank=False, null=True, default="1")
	occupation = models.CharField(max_length=200, blank=False, null=True, default="1")
	mailalert = models.BooleanField(default=False, verbose_name='Read')
	zipcode = models.CharField(max_length=50, blank=False, null=True, default="1")
	city = models.CharField(max_length=100, blank=False, null=True)
	area = models.CharField(max_length=100, blank=False, null=True)

class FriendRequests(models.Model):
    user = models.OneToOneField(User, unique=True, blank=True, null=True, verbose_name='User', on_delete=models.CASCADE)
    newrequests = models.TextField(blank=True,null=True)

class SendRequests(models.Model):
    user = models.OneToOneField(User, unique=True, blank=True, null=True, verbose_name='User', on_delete=models.CASCADE)
    newrequests = models.TextField(blank=True,null=True)

class ContactUs(models.Model):
	name = models.CharField(max_length=200, blank=False, null=True)
	email = models.CharField(max_length=200, blank=False, null=True)
	subject = models.CharField(max_length=200, blank=False, null=True)
	msg = models.CharField(max_length=500, blank=False, null=True)

	def __str__(self):
		return self.subject
