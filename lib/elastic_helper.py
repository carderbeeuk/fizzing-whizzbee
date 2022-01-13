import uuid
import traceback
from elasticsearch import Elasticsearch, helpers
from django.conf import settings
from django.core.paginator import Paginator
from lib import event_manager, utils
from apps.elasticsearch.models import Index
from apps.products.models import Product


class ElasticHelper():
    def __init__(self):
        self._init_instance()

    def _init_instance(self):
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
                docs = [utils.serialize_offer(offer) for offer in docs_paginator.page(page_num + 1).object_list]
                self._index_docs(docs, new_index_name)

            # event_manager.trigger('index-docs', threaded=False, max_threads=4)

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

    def _get_active_indices(self, provider=None):
        if not provider:
            active_indices_query_set = Index.objects.filter(active=True)
        else:
            active_indices_query_set = Index.objects.filter(active=True, provider=provider)
        return active_indices_query_set

    def _get_docs_paginator(self, provider):
        print('getting the offers paginator')
        offers = Product.objects.filter(provider=str(provider).upper(), active=True)
        p = Paginator(offers, settings.ELASTICSEARCH_PAGINATOR_PER_PAGE)
        return p

    # @event_manager.attach('index-docs')
    def _index_docs(self, docs, index_name):
        helpers.bulk(
            self.instance,
            docs,
            index=index_name
        )

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

    def delete_index(self, index):
        if self.instance.indices.exists(index=index.name):
            self.instance.indices.delete(index=index.name)