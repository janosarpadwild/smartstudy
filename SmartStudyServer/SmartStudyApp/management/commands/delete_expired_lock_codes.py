from django.core.management.base import BaseCommand
from SmartStudyApp.models import LockAccount
from django.utils import timezone

class Command(BaseCommand):
    help = 'Deletes expired lock codes'

    def handle(self, *args, **kwargs):
        # Delete expired tokens
        expired_lock_codes = LockAccount.objects.filter(expiration_time__lt=timezone.now())
        expired_lock_codes.delete()
        self.stdout.write(self.style.SUCCESS('Expired lock codes deleted successfully.'))