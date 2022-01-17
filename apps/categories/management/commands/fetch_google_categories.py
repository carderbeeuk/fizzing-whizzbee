import requests
import logging
from django.core.management.base import BaseCommand
from apps.categories.parsers.categories_parser import CategoriesParser
from apps.categories.models import Category, GoogleCategory


logger = logging.getLogger('categories')


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        categories_list = self._fetch_categories_list()
        self._update_google_categories(categories_list)
        logger.info('done updating')

    def _fetch_categories_list(self) -> list:
        logger.info('fetching')
        url = 'https://www.google.com/basepages/producttype/taxonomy-with-ids.en-GB.txt'
        content = requests.get(url).content
        parser = CategoriesParser(content)
        parsed_categories = parser.parse_google()

        return parsed_categories


    def _update_google_categories(self, categories_list):
        """
            categories_list: [{
                'id': 3415,
                'categories': [
                    'Vehicles & Parts',
                    'Vehicle Parts & Accessories',
                    'Watercraft Parts & Accessories',
                    'Watercraft Fuel Systems',
                    'Watercraft Fuel Lines & Parts'
                ]
            }, ... ]
        """

        logger.info('inserting')
        for category in categories_list:
            cat_to_insert_name = category['categories'][-1]
            parent_category = GoogleCategory.objects.filter(
                name=category['categories'][-2],
                cardinality=len(category['categories']) - 1
            ) if len(category['categories']) > 1 else [None]

            updated_category = GoogleCategory.objects.get_or_create(
                name=cat_to_insert_name,
                cardinality=len(category['categories']),
                parent_category=parent_category[0],
                google_category_id=category['id'],
                google_category_full_path=' > '.join(category['categories'])
            )