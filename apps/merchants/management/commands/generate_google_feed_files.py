import logging
import os
import csv
from django.core.management.base import BaseCommand
from apps.merchants.models import GoogleMerchantCenterAccount
from apps.products.models import Product


logger = logging.getLogger('merchants')
feeds_dir = '/srv/fizzing-whizzbee/feeds/'


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        logger.info('starting google merchant feed generation')

        google_mca_list = GoogleMerchantCenterAccount.objects.filter(active=True)
        for account in google_mca_list:
            logger.info(f'dealing with merchant "{account.merchant.name}"')
            self._remove_old_files(account)
            self._generate_new_files(account)

    def _remove_old_files(self, account):
        filepath = f'{feeds_dir}{account.account_id}_primary.tsv'
        if os.path.exists(filepath):
            logger.info(f'removing file at "{filepath}"')
            os.remove(filepath)

    def _generate_new_files(self, account):
        products = Product.objects.filter(
            google_shopping_active=True,
            active=True,
            merchant=account.merchant
        )

        if not products:
            logger.info(f'no products found for "{account.merchant.name}", skipping file generation')
            return

        output_filepath = f'{feeds_dir}{account.account_id}_primary.tsv'
        keys, rows = self._get_keys_and_rows(products)

        with open(output_filepath, 'w') as out_file:
            writer = csv.DictWriter(out_file, keys, delimiter='\t')
            writer.writeheader()
            writer.writerows(rows)

    def _get_keys_and_rows(self, products):
        keys = [
            'id',
            'title',
            'description',
            'link',
            'image_link',
            'availability',
            'price',
            'expiration_date', # should be YYYY-MM-DDThh:mmZ
            'brand',
            'gtin',
            'identifier_exists', # should be yes/no
            'condition',
            'custom_label_0',
            'custom_label_1',
            'custom_label_2',
            'custom_label_3',
            'custom_label_4',
            'shipping(country:price:min_transit_time:max_transit_time)',
        ]

        rows = [{
            'id': product.product_uuid,
            'title': product.title,
            'description': product.description,
            'link': product.merchant_landing_url,
            'image_link': product.image_large,
            'availability': str(product.availability).lower(),
            'price': f'{product.price} GBP',
            'expiration_date': None, # should be 48 hours from now
            'brand': product.manufacturer,
            'gtin': product.global_identifier,
            'identifier_exists': 'yes',
            'condition': str(product.condition).lower() if product.condition else 'new',
            'custom_label_0': None,
            'custom_label_1': None,
            'custom_label_2': None,
            'custom_label_3': None,
            'custom_label_4': None,
            'shipping(country:price:min_transit_time:max_transit_time)': product.google_shopping_delivery,
        } for product in products]

        return keys, rows