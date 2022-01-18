from rest_framework.decorators import api_view
from rest_framework.response import Response
from apps.products.models import Product
from lib import utils


@api_view(['GET'])
def single_view(request, *args, **kwargs):
    """get a single product by uuid"""

    uuid = kwargs.get('uuid', None)
    product = Product.objects.get(product_uuid=uuid)
    if not product.active:
        product.availability = 'CHECK_SITE'

    offers = Product.objects.filter(product_code=product.product_code)
    for offer in offers:
        if not offer.active:
            offer.availability = 'CHECK_SITE'

    response = {
        'product': utils.serialize_offer(product),
        'offers': [utils.serialize_offer(offer) for offer in offers],
        'offer_count': len(offers)
    }

    return Response(response)