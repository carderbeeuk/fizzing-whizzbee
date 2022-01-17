import logging
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

        file_data = self.get_file_data()
        try:
            merchant_name = str(next(file_data)['merchant_name']).strip()
        except Exception as err:
            logger.exception(err)
            return []

        self.merchant_obj = Merchant.objects.filter(
            name=merchant_name
        ).first()

        if not self.merchant_obj:
            logger.warning(f'could not find a merchant by the name {merchant_name}')
            return []

        offers = [self._parse_row(row) for row in file_data]

        return offers

    def _parse_row(self, row) -> dict:
        """parses the row into readable dict and returns"""

        ean = str(row['code_ean']) if row['code_ean'] else None
        sku = str(row['code_sku']) if row['code_sku'] else None
        mpn = str(row['code_mpn']) if row['code_mpn'] else None
        product_code = utils.build_product_code(
            ean=ean,
            sku=sku,
            mpn=mpn
        )

        if not product_code:
            return

        if row['merchant_name'] in self.inactive_merchants:
            return

        if not row['brand_name']:
            return

        if not row['google_product_category_id']:
            return
        else:
            google_category_obj = GoogleCategory.objects.get(google_category_id=row['google_product_category_id'])

        if not row['delivery_cost']:
            row['delivery_cost'] = 0

        if not row['rebate_percentage']:
            row['rebate_percentage'] = 0

        if not row['month_price']:
            row['month_price'] = 0
        
        if row['availability_status'] == 'preorder':
            row['availability_status'] = 'pre_order'

        offer = {
            'product_code': product_code,
            'active': True,
            'offer_id': row['offer_id'],
            'availability': str(row['availability_status']).upper(),
            'title': row['title'],
            'description': row['description'],
            'author': None,
            'publisher': None,
            'price': float(row['price']),
            'price_without_rebate': float(row['price_without_rebate']),
            'month_price': float(row['month_price']),
            'manufacturer': row['brand_name'],
            'merchant': self.merchant_obj,
            'google_category': google_category_obj,
            'condition': 'new',
            'click_out_url': row['go_url'],
            'merchant_landing_url': row['offer_url_landing_url'],
            'merchant_mobile_landing_url': row['offer_url_mobile_landing_url'],
            'image_large': row['image_zoom_url'],
            'image_small': row['image_url'],
            'delivery_time': row['time_to_deliver'],
            'delivery_cost': float(row['delivery_cost']),
            'discount_percentage': float(row['rebate_percentage']),
            'currency': 'GBP',
            'country': 'UK',
            'features': None,
            'provider': 'KELKOO',
        }

        return offer