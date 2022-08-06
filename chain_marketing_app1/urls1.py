from rest_framework import routers
from chain_marketing_app.models import City
from chain_marketing_app.views.delivery import delivery
from .views.views import (
    MemberAccountViewset,
    ActiveMemberViewset,
    AddProductViewset,
    ImageViewset,
    OrderViewset,
    LevelViewset,
    count,
    admin,
    IntroducerViewset,
    member_info,
    member,
    ActivationKeysViewset,
    OrderDetailsViewset,
    seller_dashboard,
    ActiveSellerViewset,
    DistrictViewset,
    TalukaViewset,
    mbw_user_details,
    get_introducer,
    get_distributers,
    direct_members,
    SubProductsStockViewset,
    BankDetailsViewset,
    CityViewset,
    SubProductsSaleViewset,
)
from chain_marketing_app.views.StockTransfer import StockTransferViewset
from chain_marketing_app.views.sale import SaleViewset,MySalesViewset,GetMembersViewset
from chain_marketing_app.views.get_heirachy import GetHeirachy
from chain_marketing_app.views.stock  import StockViewset
from chain_marketing_app.views.payout  import PayoutViewset
from chain_marketing_app.views.delivery  import delivery
from chain_marketing_app.views.admin_payout import AdminPayoutViewset
from django.urls import path
from django.urls import include
from .views.active import AcitveSellerViewset
router = routers.DefaultRouter()
router.register('member', MemberAccountViewset)
router.register('active/member', ActiveMemberViewset)
router.register('order', OrderViewset)
router.register('mbw-product', AddProductViewset)
router.register('imagesa', ImageViewset)
router.register('downline', GetHeirachy)
router.register('sale', SaleViewset)
router.register('level', LevelViewset)
router.register('stock', StockViewset)
router.register('mysales', MySalesViewset)
router.register('payout', PayoutViewset)
router.register('order-details', OrderDetailsViewset)
router.register('seller', AcitveSellerViewset)
router.register('introducer', IntroducerViewset)
router.register('active_seller', ActiveSellerViewset)
router.register('stock-transfer', StockTransferViewset)
router.register('district', DistrictViewset)
router.register('taluka', TalukaViewset)
router.register('city', CityViewset)
router.register('bank-details', BankDetailsViewset)
router.register('assign-key', ActivationKeysViewset)
router.register('sub-product-stock', SubProductsStockViewset)
router.register('make-payments',AdminPayoutViewset)
router.register('spsale',SubProductsSaleViewset)

urlpatterns = [
    path('', include(router.urls)),
    path('count/', count),
    path('admin/', admin),
    path('name/', member),
    path('member-details/', mbw_user_details),
    path('delivery/', delivery),
    path('member-info/', member_info),
    path('seller_dashboard/', seller_dashboard),
    path('direct_members/', direct_members),
    path('get_introducer/', get_introducer),
    path('get_distributers/', get_distributers),
]
