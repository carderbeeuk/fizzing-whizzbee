import logging
from django.core.management.base import BaseCommand
from lib.elastic_helper import ElasticHelper


logger = logging.getLogger('elastic')

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
        logger.info(f'indexing offers for {provider}')

        helper = ElasticHelper()
        helper.bulk_index(provider)