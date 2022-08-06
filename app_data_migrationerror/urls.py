from rest_framework import routers
from .views import ActiveUserViewset,SMSViewset
router = routers.DefaultRouter()
router.register('activate', ActiveUserViewset)
router.register('sms', SMSViewset)

urlpatterns = router.urls