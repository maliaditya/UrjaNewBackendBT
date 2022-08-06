from .imports import *

class AcitveSellerViewset(viewsets.ModelViewSet):
    queryset = ActiveSeller.objects.all()
    serializer_class = SellersSerializer
    authentication_classes = []
    permission_classes = []
    # filter_backends = [filters.SearchFilter,DjangoFilterBackend]
    # filterset_fields = [ 'member']
    # search_fields = ['member']
    