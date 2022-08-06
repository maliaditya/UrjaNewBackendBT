from .imports import *


@api_view(['PATCH'])
@permission_classes([])
def delivery(request):

    if request.method == 'Patch':
        body = request.data
        return Response(body)   