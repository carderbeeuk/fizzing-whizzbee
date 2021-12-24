import importlib
import pathlib
from django.core.management.base import BaseCommand
from django.conf import settings
from optparse import make_option
from apps.merchants.helpers.downloader import Downloader
from apps.merchants.models import Merchant


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            '-p',
            '--provider',
            dest='provider',
            type=str,
            help='The provider for which to download merchants'
        )

    def handle(self, *args, **kwargs):
        if not kwargs.get('provider'):
            self.stderr.write('Please specify a --provider')
            return

        print('setting up required directories')
        provider = kwargs.get('provider')
        
        self._download_merchants_info(provider)
        self._store_merchant_info(provider)

        print(f'done fetching {provider} merchants')

    def _download_merchants_info(self, provider):
        """downloads merchants info file"""

        file_dir = str(settings.FEED_DATA['file_dir']) + '/' + provider
        pathlib.Path(file_dir).mkdir(exist_ok=True)

        print(f'downloading {provider} merchants csv file')
        file_full_path = file_dir + '/merchants.csv'

        token = settings.PROVIDERS[provider]['api_key']
        endpoint = settings.PROVIDERS[provider]['merchants_endpoint']
        headers = {}
        if provider == 'kelkoo':
            endpoint += '?country=uk&format=csv&offerMatch=any&merchantMatch=any'
            headers = {
                'Authorization': f'Bearer {token}',
                'Accept-Encoding': 'gzip',
            }

        elif provider == 'awin':
            endpoint += token

        downloader = Downloader(endpoint, headers)
        downloader.download(file_full_path)

    def _store_merchant_info(self, provider):
        """stores merchant information in the db"""

        