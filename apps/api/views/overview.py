from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def list_view(request):
    api_urls = {
        '/api': 'overview (this page)',
        '/api/product/search/<str:search_term>': 'search for products by search term',
        '/api/product/single/<int:pk>': 'get a single product by primary key',
    }
    return Response(api_urls)