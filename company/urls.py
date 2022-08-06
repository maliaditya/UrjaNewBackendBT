from rest_framework import routers
from .views import CompanyViewset, company
from django.urls import path
from django.urls import include

router = routers.DefaultRouter()
router.register('company', CompanyViewset)



urlpatterns = [
    path('', include(router.urls)),
    path('company-info/', company),

]
