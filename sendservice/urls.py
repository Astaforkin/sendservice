from rest_framework.routers import DefaultRouter

from django.contrib import admin
from django.urls import include, path
# from rest_framework.authtoken import views

from mailing.views import MailingViewSet, ClientViewSet, MessageViewSet


router = DefaultRouter()

router.register('mailings', MailingViewSet)
router.register('clients', ClientViewSet)
router.register('messages', MessageViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include(router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]
