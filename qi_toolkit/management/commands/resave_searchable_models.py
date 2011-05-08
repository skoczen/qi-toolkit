from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.management import call_command
import subprocess
from os.path import abspath, join

from qi_toolkit.models import resave_searchable_models

class Command(BaseCommand):
    help = "Repopulate the search caches."
    __test__ = False

    def handle(self, *args, **options):
        resave_searchable_models()