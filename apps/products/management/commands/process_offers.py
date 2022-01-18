import os
import csv
import importlib
import logging
import traceback
import time
from django.conf import settings
from django.core.management.base import BaseCommand
from apps.products.models import Product
from lib import event_manager


logger = logging.getLogger('products')


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

        provider = kwargs.get('provider')
        logger.info(f'starting file processing for {provider}')

        file_dir = str(settings.FEED_DATA['file_dir']) + '/' + provider
        files_list = [f for f in os.listdir(file_dir) if f != 'merchants.csv']
        logger.info(f'found {len(files_list)} files to process')

        # set all products as inactive for now to avoid indexing inactive
        # products later on
        logger.info(f'setting active state on current products for {provider} to false')
        Product.objects.filter(provider=str(provider).upper()).update(active=False)

        logger.info('processing files')
        for f in files_list:
            self._process_file(f, file_dir, provider)
    
        event_manager.trigger('process-merchant-feed', max_threads=16)

    @event_manager.attach('process-merchant-feed')
    def _process_file(self, f, file_dir, provider):
        """processes the file and adds rows to the products table"""

        try:
            start = time.time()
            with open(file_dir + '/' + f) as file_obj:
                parser = importlib.import_module(f'apps.products.services.{provider}').Parser(file_obj)
                parser.set_inactive_merchants()
                offers = parser.get_parsed_rows()
                for offer in offers:
                    parser.store_offer(offer)
            
            end = time.time()
            time_taken = end - start
            logger.info(f'processed {len(offers)} offers for {f}, time taken: {round(time_taken)}s')

        except Exception as err:
            logger.error(f'we encountered a problem processing {f}')
            logger.exception(traceback.format_exc())