from lib2to3.pytree import Base
import logging
import csv
from django.core.management.base import BaseCommand
from apps.merchants.models import Merchant


logger = logging.getLogger('merchants')


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        logger.info('generating active merchants csv file')
        self._generate_file()

    def _generate_file(self):
        merchants = Merchant.objects.filter(
            active=True,
            approved=True
        ).exclude(source='KELKOO_PLA')

        outfile_path = '/srv/fizzing-whizzbee/files/active_merchants.csv'
        with open(outfile_path, 'w') as f:
            writer = csv.writer(f)
            writer.writerows([
                str(merchant.domain).replace('https://', ''), str(merchant.name).replace('Ltd.', '').strip(), 'GB'
            ] for merchant in merchants if merchant.domain)