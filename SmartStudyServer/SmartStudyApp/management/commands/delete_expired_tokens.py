from django.core.management.base import BaseCommand
from SmartStudyApp.models import CustomToken

class Command(BaseCommand):
    help = 'Deletes expired custom tokens'

    def handle(self, *args, **kwargs):
        # Delete expired tokens
        expired_tokens = CustomToken.objects.filter(used=True)
        expired_tokens.delete()
        self.stdout.write(self.style.SUCCESS('Expired tokens deleted successfully.'))