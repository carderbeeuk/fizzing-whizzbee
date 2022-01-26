from .processor import Processor
from apps.merchants.models import Merchant
from lib import utils


class Parser(Processor):
    def __init__(self, file_obj):
        super().__init__(file_obj)

    def get_parsed_rows(self) -> list:
        """gets offer rows from the file data and parses them"""

        file_data = self.get_file_data()
        self.merchant_obj = Merchant.objects.filter(
            name=next(file_data)['merchant_name']
        ).first()

        offers = [self._parse_row(row) for row in file_data]

        return offers

    def _parse_row(self, row) -> dict:
        """parses the row into readable dict and returns"""

        mpn = str(row['mpn']) if row['mpn'] else int(row['aw_product_id'])

        gtin = None
        try:
            gtin = str(float(row['product_GTIN']))[0:-2]
        except Exception as err:
            print(err.args)

        ean = str(row['ean']) if row['ean'] else None
        if ean == '0':
            ean = None
        upc = str(row['upc']) if row['upc'] else None
        isbn = str(row['isbn']) if row['isbn'] else None
        product_code = utils.build_product_code(
            ean=ean,
            mpn=mpn,
            gtin=gtin,
            upc=upc,
            isbn=isbn
        )

        global_identifier = None
        if gtin:
            global_identifier = gtin
        if not global_identifier and ean:
            global_identifier = ean
        if not global_identifier and isbn:
            global_identifier = isbn
        if not global_identifier and upc:
            global_identifier = upc

        if not product_code:
            return

        if row['merchant_name'] in self.inactive_merchants:
            return

        if not row['search_price']:
            return

        availability_status = 'IN_STOCK' if row['in_stock'] == '1' else 'OUT_OF_STOCK'
        if row['pre_order'] == '1':
            availability_status = 'PRE_ORDER'

        author = None
        publisher = None
        if row['merchant_id'] == '3787': # waterstones (todo: chunk this)
            if row['specifications']:
                spec_parts = row['specifications'].split('|')
                author = spec_parts[0]
                book_type = spec_parts[1]
                publisher = spec_parts[2]
                row['brand_name'] = publisher
                row['product_name'] += f' by {author} - {book_type}'

        if not row['brand_name']:
            row['brand_name'] = row['merchant_name']

        if ':' in row['delivery_cost']:
            delivery_parts = row['delivery_cost'].split(':')
            row['delivery_cost'] = str(delivery_parts[:-1]).replace('GBP', '').strip()
        
        if row['delivery_cost'] == '':
            row['delivery_cost'] = None

        try:
            delivery_cost_tmp = float(row['delivery_cost'])
        except Exception as err:
            row['delivery_cost'] = None

        if not row['savings_percent']:
            row['savings_percent'] = 0

        if not row['rrp_price'] or row['rrp_price'] == 'In Stock':
            row['rrp_price'] = row['search_price']
        
        row['rrp_price'] = row['rrp_price'].replace('£', '').replace('GBP', '').replace(',', '').strip()

        if len(row['product_name']) > 255:
            row['product_name'] = row['product_name'][:255]

        offer = {
            'product_code': product_code,
            'active': True,
            'offer_id': row['aw_product_id'],
            'availability': availability_status,
            'title': row['product_name'],
            'description': row['description'],
            'author': author,
            'publisher': publisher,
            'price': float(row['search_price']),
            'price_without_rebate': float(row['rrp_price']),
            'month_price': None,
            'manufacturer': row['brand_name'],
            'merchant': self.merchant_obj,
            'google_category': self.merchant_obj.default_google_category,
            'condition': row['condition'],
            'click_out_url': row['aw_deep_link'],
            'merchant_landing_url': row['merchant_deep_link'],
            'merchant_mobile_landing_url': row['merchant_deep_link'],
            'image_large': row['image_url'],
            'image_small': row['aw_image_url'],
            'delivery_time': row['delivery_time'],
            'delivery_cost': row['delivery_cost'],
            'discount_percentage': float(row['savings_percent']),
            'currency': 'GBP',
            'country': 'UK',
            'features': None,
            'provider': 'AWIN',
            'global_identifier': global_identifier,
        }

        return offer