from django.core.management.base import BaseCommand
from services import serve


class Command(BaseCommand):
    help = 'Run the gRPC server'

    def handle(self, *args, **kwargs):
        serve()
