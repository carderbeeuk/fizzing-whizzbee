import importlib
import pathlib
import csv
from django.core.management.base import BaseCommand
from django.conf import settings
from optparse import make_option
from lib.downloader import Downloader
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

        file_dir = str(settings.FEED_DATA['file_dir']) + '/' + provider
        pathlib.Path(file_dir).mkdir(exist_ok=True)
        file_full_path = file_dir + '/merchants.csv'
        
        self._download_merchants_info(provider, file_full_path)
        self._store_merchant_info(provider, file_full_path)

        print(f'done fetching {provider} merchants')

    def _download_merchants_info(self, provider, file_full_path):
        """downloads merchants info file"""

        print(f'downloading {provider} merchants csv file')

        token = settings.PROVIDERS[provider]['api_key']
        endpoint = settings.PROVIDERS[provider]['merchants_endpoint']
        headers = {}
        if provider == 'kelkoo':
            headers = {
                'Authorization': f'Bearer {token}',
                'Accept-Encoding': 'gzip',
            }

        elif provider == 'awin':
            endpoint += token

        downloader = Downloader(endpoint, headers)
        downloader.download(file_full_path)

    def _store_merchant_info(self, provider, file_full_path):
        """stores merchant information in the db"""

        print(f'storing merchant information for {provider}')

        provider_service = importlib.import_module(f'apps.merchants.services.{provider}').Service()

        with open(file_full_path) as f:
            reader = csv.DictReader(f)

            Merchant.objects.filter(source=str(provider).upper()).update(approved=False)
            for row in reader:
                parsed_row = provider_service.parse_row(row)
                provider_service.store_merchant(parsed_row)