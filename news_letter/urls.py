from rest_framework import routers
from .views import NewsLetterViewset
router = routers.DefaultRouter()
router.register('news_letter', NewsLetterViewset)

urlpatterns = router.urls