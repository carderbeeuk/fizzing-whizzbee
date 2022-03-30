from apps.merchants.models import Merchant
from django.db.utils import IntegrityError


class Provider():
    def __init__(self, source):
        self.source = source

    def store_merchant(self, merchant):
        "stores the merchant in the db"

        if not merchant['approved']:
            return

        try:
            merchant_obj = Merchant.objects.create(
                name=merchant['name'],
                source=merchant['source'],
                feed_name=merchant['feed_name'],
                feed_url=merchant['feed_url'],
                approved=merchant['approved']
            )

        except IntegrityError as err:
            merchant_obj = Merchant.objects.filter(
                name=merchant['name'],
                source=merchant['source'],
                feed_name=merchant['feed_name']
            ).first()
            merchant_obj.feed_url = merchant['feed_url']
            merchant_obj.approved = merchant['approved']
            merchant_obj.save()

        finally:
            if self.source == 'KELKOO':
                merchant_obj.domain = merchant['domain'] if not merchant_obj.domain else merchant['domain']
                merchant_obj.save()