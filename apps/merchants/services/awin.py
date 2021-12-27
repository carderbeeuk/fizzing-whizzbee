from .provider import Provider
from apps.merchants.models import SOURCES


class Service(Provider):
    def __init__(self):
        super().__init__('AWIN')

    def parse_row(self, row) -> dict:
        """parses the row into dict"""

        head, sep, tail = row['URL'].partition('/columns/')
        columns = [
            'aw_deep_link',
            'image_url',
            'large_image',
            'aw_image_url',
            'merchant_id',
            'merchant_name',
            'brand_id',
            'category_name',
            'category_id',
            'aw_product_id',
            'merchant_deep_link',
            'product_id', # not mpn
            'product_name',
            'search_price',
            'alternate_image',
            'brand_name',
            'condition',
            'currency',
            'delivery_cost',
            'delivery_time',
            'description',
            'ean',
            'in_stock',
            'last_updated',
            'merchant_category',
            'merchant_product_category_path',
            'mpn',
            'pre_order',
            'product_GTIN',
            'rrp_price',
            'savings_percent',
            'upc',
            'google_taxonomy',
            'author',
            'publisher',
            'specifications',
            'rating',
            'product_type',
            'merchant_product_category_path',
            'keywords',
            'isbn',
        ]
        feed_url = head + sep + ','.join(columns)

        merchant = {
            'name': row['Advertiser Name'].strip(),
            'source': self.source,
            'feed_name': row['Feed Name'].strip(),
            'feed_url': feed_url,
            'approved': row['Membership Status'] == 'active'
        }

        return merchant