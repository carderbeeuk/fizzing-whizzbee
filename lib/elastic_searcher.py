from .elastic_helper import ElasticHelper


class ElasticSearcher(ElasticHelper):
    def __init__(self):
        super().__init__()

    def _append_to_query(self, params):
        """appends to main query if params exist"""

        if params['brand']:
            self.must_match_query.append({
                "match": {
                    "manufacturer": params['brand']
                }
            })

        if params['delivery']:
            if params['delivery'] == 'Free delivery':
                self.must_match_query.append({
                    "match": {
                        "delivery_cost": 0
                    }
                })

    def _set_sorting(self, params):
        if params['price_sort']:
            self.aggs["sales_bucket_sort"] = {
                "bucket_sort": {
                    "sort": [
                        { "min_price": { "order": params['price_sort'] } } 
                    ]
                }
            }

    def _build_main_aggregation_query(self, params, build_type=None):
        main_match_query = self.must_match_query
        if build_type == 'category':
            main_match_query = self.category_offers_must_match_query
        query = {
            "size": 0,
            "query": {
                "bool": {
                    "must": main_match_query,
                    "filter": [
                        {
                            "range" : {
                                "price" : { "gte" : params['min_price'], "lte" : params['max_price'] }
                            }
                        }
                    ],
                    "must_not": []
                }
            },
            "aggs": {
                "product_code_agg": {
                    "terms": {
                        "field": "product_code.keyword",
                        "min_doc_count": 1,
                        "order": {
                            "max_score": "desc"
                        },
                        "size": params['limit']
                    },
                    "aggs": self.aggs
                }
            }
        }

        return query

    def _build_products_list(self, aggs, params, active_indices):
        products = []
        for agg in aggs:
            offers_query = { 
                "size": params['limit'],
                "from": params['start'], 
                "query": {
                    "multi_match": {
                        "query": agg['key'],
                        "fields": ["product_code"],
                        "minimum_should_match": "100%"
                    }
                },
                "sort": [
                    { "price": "asc" }
                ]
            }
            try:
                offers_result = self.instance.search(index=[index.name for index in active_indices], body=offers_query)
                offers = [offer for offer in offers_result['hits']['hits']]
                products.append({
                    'product': offers[0],
                    'offer_count': offers_result['hits']['total']['value'],
                    'offers': offers
                })

            except Exception as err:
                print(err)
        
        return products

    def _valid(self, agg) -> bool:
        """checks if aggregation is valid"""

        valid = True

        if agg['max_score']['value'] / agg['doc_count'] < 1:
            valid = False

        if agg['doc_count'] > 25:
            valid = False

        return valid

    def _reset_queries(self):
        self.must_match_query = [
            {
                "multi_match": {
                    "fields": ["title^3", "google_category^2", "manufacturer"],
                    "operator": "and",
                    "minimum_should_match": "100%",
                    "fuzziness": 1,
                    "prefix_length": 4
                }
            }
        ]

        self.category_offers_must_match_query = [
            {
                "term": {
                    "google_category.keyword": None
                }
            }
        ]

        self.aggs = {
            "max_score": {
                "sum": {
                    "script": "_score"
                }
            },
            "min_price": {
                "min": {
                    "field": "price"
                }
            }
        }

    def _handle_category_selection(self, params):
        if params['category']:
            self.must_match_query.append({
                "match": {
                    "google_category": params['category']
                }
            })

    def search(self, params):
        """search for grouped offers by term"""

        terms = [f'{term}' for term in params['search_term'].split()]
        query_search_term = ' '.join(terms) + '~'
        active_indices = self._get_active_indices()

        self._reset_queries()
        self.must_match_query[0]['multi_match']['query'] = query_search_term
        self._append_to_query(params)
        self._handle_category_selection(params)  
        self._set_sorting(params)

        main_aggregation_query = self._build_main_aggregation_query(params)
        main_aggregation_result = self.instance.search(index=[index.name for index in active_indices], body=main_aggregation_query)
        aggs = [agg for agg in main_aggregation_result['aggregations']['product_code_agg']['buckets'] if self._valid(agg)]

        return self._build_products_list(aggs, params, active_indices)

    def category_offers(self, params):
        """get offers by category"""

        category_name = params['category_name']
        active_indices = self._get_active_indices()
        self._reset_queries()
        self.category_offers_must_match_query[0]['term']['google_category.keyword'] = category_name
        self._append_to_query(params)
        self._handle_category_selection(params)
        self._set_sorting(params)

        main_aggregation_query = self._build_main_aggregation_query(params, 'category')
        main_aggregation_result = self.instance.search(index=[index.name for index in active_indices], body=main_aggregation_query)
        aggs = [agg for agg in main_aggregation_result['aggregations']['product_code_agg']['buckets'] if self._valid(agg)]

        return self._build_products_list(aggs, params, active_indices)