from django.shortcuts import render, HttpResponseRedirect
from django.http import HttpResponse
from django.views.generic import TemplateView, View

# Create your views here.
class TheBridge(TemplateView):
	template_name = 'thebridge.html'
	def get(self, request, *args, **kwargs):
		return render(request, self.template_name,{})
