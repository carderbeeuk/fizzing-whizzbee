from .provider import Provider
from apps.merchants.models import SOURCES


class Service(Provider):
    def __init__(self):
        super().__init__('KELKOO_PLA')

    def parse_row(self, row) -> dict:
        """parses the row into dict"""

        feed_url = f'https://api.kelkoogroup.net/publisher/shopping/v2/feeds/pla?format=csv&fieldsAlias=all&country=uk&merchantId={row["id"]}'
        merchant = {
            'name': str(row['name']).strip(),
            'source': self.source,
            'feed_name': 'Default',
            'feed_url': feed_url,
            'approved': True,
            'domain': self._get_domain(row['url']),
        }

        return merchant

    def _get_domain(self, url):
        domain = str(url).replace('http://', 'https://').replace('www.', '')
        domain = domain.split('?')[0]
        if domain.count('/') > 2:
            parts = domain.split('/')
            domain = f'{parts[0]}//{parts[2]}'
        return domain