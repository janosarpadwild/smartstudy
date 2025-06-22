from django.core.management.base import BaseCommand
from SmartStudyApp.models import PermissionCode
from django.utils import timezone

class Command(BaseCommand):
    help = 'Deletes expired permission codes'

    def handle(self, *args, **kwargs):
        # Delete expired tokens
        expired_permission_codes = PermissionCode.objects.filter(expiration_time__lt=timezone.now())
        expired_permission_codes.delete()
        self.stdout.write(self.style.SUCCESS('Expired permission codes deleted successfully.'))