
from django.contrib import admin
from django.urls import path
from django.conf.urls import url,include
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
     url(r'^', include('main.urls')),
     url(r'^chat/', include('chat.urls')),
     url(r'^bridge/', include('thebridge.urls')),
     url(r'^prize/', include('prize.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += staticfiles_urlpatterns()
if settings.DEBUG is False:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += staticfiles_urlpatterns()
