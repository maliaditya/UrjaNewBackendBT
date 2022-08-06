from rest_framework import routers
from .views import (ProductsViewset, ProductTypeViewset, CategoriesViewset, ReviewViewset, FavouriteProductViewset,SearchProductViewset,
ProductEnquiriesViewset,ProductTypeWiseCategoryViewset ,PorductNameListViewset   )
from .android_addproduct import AddProductsViewset
from django.urls import path, include, re_path

router = routers.DefaultRouter()
router.register('add_product', AddProductsViewset)
router.register('products', ProductsViewset)
router.register('categories', CategoriesViewset)
router.register('product_type', ProductTypeViewset)
router.register('review', ReviewViewset)
router.register('favourites', FavouriteProductViewset)
router.register('product_enquires', ProductEnquiriesViewset)
router.register('product', SearchProductViewset)
router.register('type_category', ProductTypeWiseCategoryViewset)
router.register('product_names', PorductNameListViewset)


urlpatterns = router.urls
