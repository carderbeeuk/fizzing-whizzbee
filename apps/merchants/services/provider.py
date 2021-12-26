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
            updated_merchant = Merchant.objects.create(
                name=merchant['name'],
                source=merchant['source'],
                feed_name=merchant['feed_name'],
                feed_url=merchant['feed_url'],
                approved=merchant['approved']
            )

        except IntegrityError as err:
            existing_merchant = Merchant.objects.filter(
                name=merchant['name'],
                source=merchant['source'],
                feed_name=merchant['feed_name']
            ).first()
            existing_merchant.feed_url = merchant['feed_url']
            existing_merchant.approved = merchant['approved']
            existing_merchant.save()