from django.shortcuts import render, HttpResponseRedirect
from django.http import HttpResponse
from django.views.generic import TemplateView, View
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.models import User
from .models import *
import json
# Create your views here.


class IndexPage(TemplateView):
	template_name = 'index.html'
	def get(self, request, *args, **kwargs):
		return render(request, self.template_name,{})

class Home(TemplateView):
	template_name = 'homepage.html'
	def get(self, request, *args, **kwargs):
		user = User.objects.get(id=request.user.id)
		profile = Profile.objects.get(user=user)
		return render(request, self.template_name,{"user":user,"profile":profile})

class ChatPage(TemplateView):
	template_name = 'chat.html'
	def get(self, request, *args, **kwargs):
		return render(request, self.template_name,{})

class Faq(TemplateView):
	template_name = 'FAQ.html'
	def get(self, request, *args, **kwargs):
		return render(request, self.template_name,{})

class ContactUsView(TemplateView):
	template_name = 'contact_us.html'
	def get(self, request, *args, **kwargs):
		return render(request, self.template_name,{})
	def post(self, request, *args, **kwargs):
		email=self.request.POST.get('email')
		name=self.request.POST.get('name')
		subject=self.request.POST.get('subject')
		msg=self.request.POST.get('message')
		contact = ContactUs(name=name,email=email,subject=subject,msg=msg)
		contact.save()
		messages.success(request,'Your request is successfully submitted.')
		return render(request, self.template_name,{})
class Login(TemplateView):
	template_name = 'user/login.html'

	def post(self, request, *args, **kwargs):
		email=self.request.POST.get('email')
		password=self.request.POST.get('pass')
		try:
			user = User.objects.get(email=email)
			userauth = authenticate(username=user.email, password=password)
			if userauth:
				login(request, user)
				return HttpResponseRedirect('homepage')
			else:
				messages.error(request,'Incorrect password address given.')
				return HttpResponseRedirect('/')
		except User.DoesNotExist:
			messages.error(request,'Incorrect email address given.')
			return HttpResponseRedirect('/')

	def get_context_data(self, *args, **kwargs):
		context = super(Login, self).get_context_data(**kwargs)
		return context

class Register(TemplateView):
	template_name = 'user/registration.html'

	def post(self, request, *args, **kwargs):
		first_name = self.request.POST.get('firstname')
		last_name = self.request.POST.get('lastname')
		email = self.request.POST.get('email')
		password = self.request.POST.get('pass')
		cpassword = self.request.POST.get('cpass')
		phone = self.request.POST.get('phone')
		age = self.request.POST.get('age')
		occupation = self.request.POST.get('occupation')
		address = self.request.POST.get('address')
		mailalert = self.request.POST.get('mailalert')
		zipcode = self.request.POST.get('pin')
		city = self.request.POST.get('city')
		area = self.request.POST.get('area')
		if mailalert:
			mailalert = True
		else:
			mailalert = False
		try:
			user = User.objects.get(email=email)
			messages.error(request,'This email already exists. Try to login.')
			return HttpResponseRedirect('/')
		except User.DoesNotExist:
			if password and cpassword and password != cpassword:
				messages.error(request,'Password is not matched.')
				return HttpResponseRedirect('register')
			user = User.objects.create_user(
				username=email,
				email=email,
				password=password
			)
			user.first_name = first_name
			user.last_name = last_name
			user.is_active = True
			user.save()
			profile = Profile(
			user=user,
			phone=phone,
			age=age,
			occupation=occupation,
			address=address,
			mailalert=mailalert,
			zipcode=zipcode,
			city=city,
			area=area
			)
			profile.save()
			userauth = authenticate(username=user.username, password=password)
			if userauth:
				login(request, user)
			return HttpResponseRedirect('homepage')

	def get_context_data(self, *args, **kwargs):
		context = super(Register, self).get_context_data(**kwargs)
		return context

class FindFriends(TemplateView):
	template_name = "findfriends.html"
	def get(self, request):
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
		users = User.objects.filter(is_staff=0, is_superuser=0).exclude(id__in=exclude_users)

		return render(request, self.template_name, {"users":users})

class AddFriend(View):
	def post(self, request):
		userid = request.POST.get("id")
		response = {}
		try:
			userrequest = FriendRequests.objects.get(user__id=int(userid))
			totalrequests = []
			if userrequest.newrequests:
				totalrequests = json.loads(userrequest.newrequests)
			totalrequests.append(request.user.id)
			userrequest.newrequests = str(totalrequests)
			userrequest.save()

		except FriendRequests.DoesNotExist:
			totalrequests = [request.user.id]
			newreq = FriendRequests(user_id=int(userid),newrequests=str(totalrequests))
			newreq.save()

		try:
			user = SendRequests.objects.get(user=request.user)
			userlist = []
			if user.newrequests:
				userlist = json.loads(user.newrequests)
			userlist.append(int(userid))
			user.newrequests = str(userlist)
			user.save()
		except SendRequests.DoesNotExist:
			userlist = [int(userid)]
			user = SendRequests(user=request.user, newrequests=str(userlist))
			user.save()
		response["status"] = "success"
		return HttpResponse(json.dumps(response),content_type='application/json')


class DeleteReceiveRequest(View):
	def post(self, request):
		userid = request.POST.get("id")
		response = {}
		user = FriendRequests.objects.get(user=request.user)
		userlist = json.loads(user.newrequests)
		userlist.remove(int(userid))
		user.newrequests = str(userlist)
		user.save()
		pendingrequests = []
		senduser = SendRequests.objects.get(user_id=int(userid))
		pendingrequests = json.loads(senduser.newrequests)
		pendingrequests.remove(request.user.id)
		senduser.newrequests = str(pendingrequests)
		senduser.save()
		response["status"] = "success"
		return HttpResponse(json.dumps(response),content_type='application/json')


class DeleteSendRequest(View):
	def post(self, request):
		userid = request.POST.get("id")
		response = {}
		user = FriendRequests.objects.get(user=int(userid))
		userlist = json.loads(user.newrequests)
		userlist.remove(int(request.user.id))
		user.newrequests = str(userlist)
		user.save()
		pendingrequests = []
		senduser = SendRequests.objects.get(user_id=request.user.id)
		pendingrequests = json.loads(senduser.newrequests)
		pendingrequests.remove(int(userid))
		senduser.newrequests = str(pendingrequests)
		senduser.save()
		response["status"] = "success"
		return HttpResponse(json.dumps(response),content_type='application/json')

class AcceptRequest(View):
	def post(self, request):
		userid = request.POST.get("id")
		response = {}
		user = FriendRequests.objects.get(user=request.user)
		userlist = json.loads(user.newrequests)
		userlist.remove(int(userid))
		user.newrequests = str(userlist)
		user.save()
		totalfriends = []
		profile = Profile.objects.get(user=request.user)
		if profile.friends:
			totalfriends = json.loads(profile.friends)
		totalfriends.append(int(userid))
		profile.friends = str(totalfriends)
		profile.save()
		pendingrequests = []
		senduser = SendRequests.objects.get(user_id=int(userid))
		pendingrequests = json.loads(senduser.newrequests)
		pendingrequests.remove(request.user.id)
		senduser.newrequests = str(pendingrequests)
		senduser.save()
		response["status"] = "success"
		return HttpResponse(json.dumps(response),content_type='application/json')

class FriendRequest(TemplateView):
	template_name = "requests.html"
	def get(self, request):
		users1=[]
		users2=[]
		try:
			incoming = FriendRequests.objects.get(user=request.user)
			requestlist1 = json.loads(incoming.newrequests)
			users1 = User.objects.filter(id__in=requestlist1)
		except Exception as e:
			pass
		try:
			outgoing = SendRequests.objects.get(user=request.user)
			requestlist2 = json.loads(outgoing.newrequests)
			users2 = User.objects.filter(id__in=requestlist2)
		except Exception as e:
			pass

		return render(request,self.template_name, {"received":users1,"send":users2})



class Friends(TemplateView):
	template_name = "friends.html"
	def get(self,request):
		fiendslist=[]
		profile = Profile.objects.get(user=request.user)
		if profile.friends:
			fiendslist = json.loads(profile.friends)
		users = User.objects.filter(id__in=fiendslist)
		return render(request, self.template_name, {"users":users})

class EditProfile(TemplateView):
	template_name = "editprofile.html"
	def get(self, request, *args, **kwargs):
		user = User.objects.get(id=request.user.id)
		profile = Profile.objects.get(user=user)
		return render(request, self.template_name,{"user":user,"profile":profile})

	def post(self, request, *args, **kwargs):
		first_name = self.request.POST.get('firstname')
		last_name = self.request.POST.get('lastname')
		email = self.request.POST.get('email')
		phone = self.request.POST.get('phone')
		age = self.request.POST.get('age')
		occupation = self.request.POST.get('occupation')
		address = self.request.POST.get('address')
		zipcode = self.request.POST.get('pin')
		try:
			user = User.objects.exclude(id=request.user.id).get(email=email)
			messages.error(request,'This email already exists.')
			return HttpResponseRedirect('homepage')
		except User.DoesNotExist:
			user = User.objects.get(id=request.user.id)
			user.username=email
			user.email=email
			user.first_name = first_name
			user.last_name = last_name
			user.save()
			profile = Profile.objects.get(user=user)
			profile.phone = phone
			profile.age = age
			profile.occupation = occupation
			profile.address = address
			profile.zipcode = zipcode
			profile.save()
			return HttpResponseRedirect('homepage')
