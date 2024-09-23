from django.core.management.base import BaseCommand
from backend.models import UserProfile


class Command(BaseCommand):
    help = 'Populates the UserProfile table with dummy data'

    def handle(self, *args, **kwargs):

        UserProfile.objects.create(
            username='user1',
            is_subscribed=True,
            subscription_area='Huston'
        )
        UserProfile.objects.create(
            username='user2',
            is_subscribed=True,
            subscription_area='Chicago'
        )
        UserProfile.objects.create(
            username='user3',
            is_subscribed=True,
            subscription_area='New York'
        )

        self.stdout.write(self.style.SUCCESS('Successfully populated UserProfile table with dummy data.'))
