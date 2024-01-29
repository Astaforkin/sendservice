from rest_framework.routers import DefaultRouter

from django.contrib import admin
from django.urls import include, path

from mailing.views import MailingViewSet, ClientViewSet, MessageViewSet


router = DefaultRouter()

router.register('mailings', MailingViewSet)
router.register('contacts', ClientViewSet)
router.register('messages', MessageViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include(router.urls)),
]
