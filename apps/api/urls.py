from django.urls import path
from .views import overview
from .views import category_offers
from .views import products_search
from .views import products_single
from .views import traffic

urlpatterns = [
    path(r'', overview.list_view, name='overview'),
    path(r'category/offers/<str:category_name>', category_offers.offers_view, name='category-offers'),
    path(r'product/search/<str:search_term>', products_search.search_view, name='product-search'),
    path(r'product/single/<str:uuid>', products_single.single_view, name='product-single'),
    path(r'traffic/redirect/<str:product_id>', traffic.redirect_view, name='traffic')
]