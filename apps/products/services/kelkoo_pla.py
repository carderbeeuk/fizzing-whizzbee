import logging
from operator import gt
from .processor import Processor
from apps.categories.models import GoogleCategory
from apps.merchants.models import Merchant
from lib import utils


logger = logging.getLogger('products')


class Parser(Processor):
    def __init__(self, file_obj):
        super().__init__(file_obj)

    def get_parsed_rows(self) -> list:
        """gets offer rows from the file data and parses them"""

        file_data = self.get_file_data(delimiter='\t')
        try:
            merchant_name = str(next(file_data)['seller_name']).strip()
        except Exception as err:
            logger.error(err.args)
            return []

        self.merchant_obj = Merchant.objects.filter(
            name=merchant_name,
            source='KELKOO_PLA'
        ).first()

        if not self.merchant_obj:
            logger.warning(f'could not find a merchant by the name {merchant_name}')
            return []

        offers = [self._parse_row(row) for row in file_data]

        return offers

    def _parse_row(self, row) -> dict:
        """parses the row into readable dict and returns"""

        gtin = str(row['gtin']) if row['gtin'] else None
        if not gtin:
            return

        mpn = str(row['mpn']) if row['mpn'] else None
        product_code = utils.build_product_code(
            gtin=gtin,
            mpn=mpn
        )

        if not product_code:
            return

        if row['seller_name'] in self.inactive_merchants:
            return

        if not row['brand']:
            return

        if not row['google_product_category']:
            return
        else:
            google_category_obj = GoogleCategory.objects.get(google_category_id=row['google_product_category'])

        if not row['shipping']:
            row['delivery_cost'] = 0

        if row['availability'] == 'in stock':
            row['availability'] = 'in_stock'
        if row['availability'] == 'preorder':
            row['availability'] = 'pre_order'
        if row['availability'] == 'out of stock':
            row['availability'] = 'out_of_stock'

        offer = {
            'product_code': product_code,
            'active': True,
            'offer_id': row['id'],
            'availability': str(row['availability']).upper(),
            'title': row['title'],
            'description': row['description'],
            'author': None,
            'publisher': None,
            'price': float(row['sale_price']) if row['sale_price'] else float(row['price']),
            'price_without_rebate': float(row['price']),
            'month_price': None,
            'manufacturer': row['brand'],
            'merchant': self.merchant_obj,
            'google_category': google_category_obj,
            'condition': row['condition'],
            'click_out_url': row['ads_redirect'],
            'merchant_landing_url': row['link'],
            'merchant_mobile_landing_url': row['link'],
            'image_large': row['image_link'],
            'image_small': row['image_link'],
            'delivery_time': self._get_delivery_info(row['shipping']),
            'delivery_cost': None,
            'discount_percentage': 0,
            'currency': 'GBP',
            'country': 'UK',
            'features': None,
            'provider': 'KELKOO_PLA',
            'global_identifier': gtin,
        }

        return offer

    def _get_delivery_info(self, shipping):
        """only returns cost right now"""
        # expecting format GB:::3.99 GBP
        parts = str(shipping).split(':')
        return str(parts[:-1]).replace('GBP', '').strip()