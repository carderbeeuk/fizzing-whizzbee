import logging
from django.core.management.base import BaseCommand
from django.conf import settings
from apps.merchants.models import Merchant
from lib.downloader import Downloader
from lib.file_handler import FileHandler
from lib import event_manager, utils


logger = logging.getLogger('merchants')


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

        logger.info('finding merchants to download feeds for')
        provider = kwargs.get('provider')
        file_dir = str(settings.FEED_DATA['file_dir']) + '/' + provider

        merchants_query_set = Merchant.objects.filter(source=str(provider).upper(), approved=True, active=True)
        for merchant in merchants_query_set:
            self._download_merchant_feed(merchant, file_dir)
        
        event_manager.trigger('download-merchant-feed', max_threads=4)

    @event_manager.attach('download-merchant-feed')
    def _download_merchant_feed(self, merchant, file_dir):
        """downloads merchant feed file"""

        logger.info(f'downloading merchant feed for {merchant.name} - {merchant.feed_name}')

        token = settings.PROVIDERS[str(merchant.source).lower()]['api_key']
        headers = {}
        if merchant.source == 'KELKOO' or merchant.source == 'KELKOO_PLA':
            headers = {
                'Authorization': f'Bearer {token}',
                'Accept-Encoding': 'gzip',
            }

        new_filename = str(merchant.name.strip() + '_' + merchant.feed_name).lower().replace(' ', '-').replace('/', '-') + f'_offer_feed.gz'
        unzipped_filename = str(merchant.name.strip() + '_' + merchant.feed_name).lower().replace(' ', '-').replace('/', '-') + f'_offer_feed.csv'

        src_file_path = file_dir + '/' + new_filename
        dest_file_path = file_dir + '/' + unzipped_filename

        # download the raw file
        downloader = Downloader(merchant.feed_url, headers)
        downloader.download(src_file_path)

        # unzip the file if needed
        file_handler = FileHandler(src_file_path, dest_file_path)
        file_handler.unzip_file()