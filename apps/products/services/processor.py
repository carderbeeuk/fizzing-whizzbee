import csv
import logging
import traceback
from apps.merchants.models import Merchant
from apps.products.models import Product
from django.db.utils import IntegrityError
from django.db.models import Q


class Processor():
    def __init__(self, file_obj):
        self.file_obj = file_obj

    def get_file_data(self):
        file_data = csv.DictReader(self.file_obj)
        return file_data

    def set_inactive_merchants(self, provider):
        inactive_merchants = Merchant.objects.filter(
            Q(active=False) | Q(approved=False)
        )
        self.inactive_merchants = [merchant.name for merchant in inactive_merchants if merchant.source == str(provider).upper()]

    def store_offer(self, offer):
        """stores the offer in the products table"""

        if not offer:
            return

        try:
            new_offer = Product.objects.create(
                product_code=offer['product_code'],
                active=offer['active'],
                offer_id=offer['offer_id'],
                availability=offer['availability'],
                title=offer['title'],
                description=offer['description'],
                author=offer['author'],
                publisher=offer['publisher'],
                price=offer['price'],
                price_without_rebate=offer['price_without_rebate'],
                month_price=offer['month_price'],
                manufacturer=offer['manufacturer'],
                merchant=offer['merchant'],
                google_category=offer['google_category'],
                condition=offer['condition'],
                click_out_url=offer['click_out_url'],
                merchant_landing_url=offer['merchant_landing_url'],
                merchant_mobile_landing_url=offer['merchant_mobile_landing_url'],
                image_large=offer['image_large'],
                image_small=offer['image_small'],
                delivery_time=offer['delivery_time'],
                delivery_cost=offer['delivery_cost'],
                discount_percentage=offer['discount_percentage'],
                currency=offer['currency'],
                country=offer['country'],
                features=offer['features'],
                provider=offer['provider'],
                global_identifier=offer['global_identifier']
            )

        except IntegrityError as err:
            existing_offer = Product.objects.filter(
                offer_id=offer['offer_id'],
                title=offer['title']
            ).first()
            existing_offer.active = True
            existing_offer.product_code = offer['product_code']
            existing_offer.global_identifier = offer['global_identifier'] if offer['global_identifier'] else existing_offer.global_identifier
            existing_offer.availability = offer['availability']
            existing_offer.save()

        except Exception as err:
            err_logger = logging.getLogger('error_mailer')
            err_logger.error(traceback.format_exc())
            exit()