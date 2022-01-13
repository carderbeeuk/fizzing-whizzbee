from rest_framework.decorators import api_view
from rest_framework.response import Response
from lib import elastic_searcher


searcher = elastic_searcher.ElasticSearcher()


@api_view(['GET'])
def offers_view(request, *args, **kwargs):
    """searches for products in a category by category name"""

    params = _get_params(request, kwargs)
    results = searcher.category_offers(params)
    return Response(results)


def _get_params(request, kwargs):
    """gets the request params in a neat dict"""

    # general
    limit = request.query_params.get('limit', 20)
    start = request.query_params.get('start', 0)
    min_price = request.query_params.get('min_price', None)
    max_price = request.query_params.get('max_price', None)
    brand = request.query_params.get('brand', None)
    category = request.query_params.get('category', None)
    delivery = request.query_params.get('delivery', None)

    # fixes
    if min_price == 'null':
        min_price = None
    if max_price == 'null':
        max_price = None
    if brand == 'null':
        brand = None
    if category == 'null':
        category = None
    if delivery == 'null' or delivery == '£0.00' or delivery == '0.00' or delivery == 0:
        delivery = None

    # sorting
    sort = request.query_params.get('sort', 'relevance')
    price_sort = None
    if sort != 'relevance':
        price_sort = 'desc'
        if sort == 'price_asc':
            price_sort = 'asc'

    params_list = {
        'limit': limit,
        'start': start,
        'price_sort': price_sort,
        'min_price': min_price,
        'max_price': max_price,
        'brand': brand,
        'category': category,
        'category_name': kwargs.get('category_name', None),
        'delivery': delivery,
    }

    return params_list