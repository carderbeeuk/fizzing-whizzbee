import logging
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import redirect
from apps.products.models import Product


@api_view(['GET'])
def redirect_view(request, *args, **kwargs):
    """redirects based on product id in kwargs"""

    product_uuid = kwargs.get('product_id', None)
    gclid = kwargs.get('gclid', None)
    try:
        product_obj = Product.objects.get(product_uuid=product_uuid)
    except Exception as err:
        logger = logging.getLogger('products')
        logger.error(f'there was a problem retrieving the product object to redirect, product id: {product_uuid}')
        return Response('no product found by that ID, could not redirect', status=400)

    click_out_url = product_obj.click_out_url + f'&pref1={gclid}&clickref={gclid}'
    return redirect(click_out_url)