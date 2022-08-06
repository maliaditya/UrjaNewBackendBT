from rest_framework import routers
from .views import (AddressViewSet, UserAccountViewSet,FAQViewSet, ReportsViewSet, UserInfoViewSet )
from django.urls import path, include, re_path

router = routers.DefaultRouter()

router.register('address', AddressViewSet)
router.register('account', UserAccountViewSet)
router.register('faqs', FAQViewSet)
router.register('reports', ReportsViewSet)
router.register('me', UserInfoViewSet)

urlpatterns = router.urls
