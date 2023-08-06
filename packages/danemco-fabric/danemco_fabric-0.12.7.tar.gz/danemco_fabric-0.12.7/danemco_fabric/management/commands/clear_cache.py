from __future__ import print_function
import logging
import six

from django.conf import settings
from django.core.management.base import BaseCommand

try:
    # new in Django 1.7
    from django.core.cache import caches
except ImportError:
    # deprecated in Django 1.7
    from django.core.cache import get_caches as caches


class Command(BaseCommand):
    help = """Clear configured django cache backends."""

    def add_arguments(self, parser):
        parser.add_argument(
            'keys',
            metavar='KEY',
            nargs='+',
            help="Specify which cache should be cleared from CACHES by key."
        )

    def handle(self, *args, **options):

        keys = options.get('keys', [])
        if keys and isinstance(keys, (list, tuple)):
            for key in keys:
                if isinstance(key, six.string_types) and key in settings.CACHES:

                    try:
                        self.stdout.write('Clearing cache for `{}`.\n'.format(key))
                        caches[key].clear()
                    except (KeyError, AttributeError,) as ex:
                        logging.error(six.text_type(ex), exc_info=True)
                else:
                    self.stdout.write('Invalid cache key: `{}`.\n'.format(key))
