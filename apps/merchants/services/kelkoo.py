from .provider import Provider
from apps.merchants.models import SOURCES


class Service(Provider):
    def __init__(self):
        super().__init__('KELKOO')

    def parse_row(self, row) -> dict:
        """parses the row into dict"""

        feed_url = f'https://api.kelkoogroup.net/publisher/shopping/v2/feeds/offers?format=csv&fieldsAlias=all&country=uk&merchantId={row["id"]}'
        merchant = {
            'name': str(row['name']).strip(),
            'source': self.source,
            'feed_name': 'Default',
            'feed_url': feed_url,
            'approved': True
        }

        return merchant