import uuid
import traceback
from elasticsearch import Elasticsearch, helpers
from django.conf import settings
from django.core.paginator import Paginator
from lib import event_manager
from apps.elasticsearch.models import Index
from apps.products.models import Product


class ElasticHelper():
    def __init__(self):
        self._init_instance()

    def _init_instance(self):
        print('intitializing es instance')
        es_url = f"{settings.ELASTICSEARCH['host']}:{settings.ELASTICSEARCH['port']}"
        if settings.APPLICATION_ENV == 'production':
            es_url = f"{settings.ELASTICSEARCH['user']}:{settings.ELASTICSEARCH['pass']}@{es_url}"

        self.instance = Elasticsearch(es_url)

    def bulk_index(self, provider, feed_name='offers'):
        print(f'starting bulk index for {provider}')
        version = str(uuid.uuid4()).split('-')[-1]
        new_index_name = f'fw_{provider}_{feed_name}_{version}'
        docs_paginator = self._get_docs_paginator(provider)

        try:
            for page_num in range(docs_paginator.num_pages):
                print(f'indexing page {page_num + 1}/{docs_paginator.num_pages} on {new_index_name}')
                docs = [self._serialize_offer(offer) for offer in docs_paginator.page(page_num + 1).object_list]
                self._index_docs(docs, new_index_name)

            event_manager.trigger('index-docs')

        except Exception as err:
            print(traceback.format_exc())
            # pass

        else:
            self._get_active_indices(provider).update(active=False)
            new_index = Index.objects.create(
                name=new_index_name,
                provider=provider
            )
            self.clean_old_indices(provider)

    def _get_active_indices(self, provider):
        print('getting active indices')
        active_indices_query_set = Index.objects.filter(active=True, provider=provider)
        return active_indices_query_set

    def _get_docs_paginator(self, provider):
        print('getting the offers paginator')
        offers = Product.objects.filter(provider=str(provider).upper(), active=True)
        p = Paginator(offers, settings.ELASTICSEARCH_PAGINATOR_PER_PAGE)
        return p

    @event_manager.attach('index-docs')
    def _index_docs(self, docs, index_name):
        helpers.bulk(
            self.instance,
            docs,
            index=index_name
        )

    def _serialize_offer(self, offer) -> dict:
        serialised_offer = {
            'product_code': offer.product_code,
            'active': offer.active,
            'product_uuid': offer.product_uuid,
            'offer_id': offer.offer_id,
            'availability': offer.availability,
            'title': offer.title,
            'description': offer.description,
            'author': offer.author,
            'publisher': offer.publisher,
            'price': offer.price,
            'price_without_rebate': offer.price_without_rebate,
            'month_price': offer.month_price,
            'manufacturer': offer.manufacturer,
            'merchant': offer.merchant.name,
            'provider': offer.provider,
            'google_category': offer.google_category.google_category_full_path,
            'condition': offer.condition,
            'click_out_url': offer.click_out_url,
            'merchant_landing_url': offer.merchant_landing_url,
            'merchant_mobile_landing_url': offer.merchant_mobile_landing_url,
            'image_large': offer.image_large,
            'image_small': offer.image_small,
            'delivery_time': offer.delivery_time,
            'delivery_cost': offer.delivery_cost,
            'discount_percentage': offer.discount_percentage,
            'currency': offer.currency,
            'country': offer.country,
        }

        return serialised_offer

    def clean_old_indices(self, provider):
        print('cleaning old indices')
        indices = Index.objects.all().order_by('-created')
        if len(indices) > 3:
            indices_to_remove = indices[3:]
            for index in indices_to_remove:
                print(f'removing index pointer for {index.name}')
                index.delete()
                if self.instance.indices.exists(index=index.name):
                    print(f'removing elastic index for {index.name}')
                    self.instance.indices.delete(index=index.name)