from django.conf import settings

def socket_url(request):
	return {'NODEJS_SOCKET_URL': settings.NODEJS_SOCKET_URL}
