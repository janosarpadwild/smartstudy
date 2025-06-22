from django.utils import timezone
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import CustomToken


class SingleUseTokenAuthentication(TokenAuthentication):
    model = CustomToken
    def authenticate_credentials(self, key):
        try:
            token = CustomToken.objects.get(key=key, used=False)
        except CustomToken.DoesNotExist:
            raise AuthenticationFailed('Unauthorized')
        # Check if the token has expired due to inactivity
        if (timezone.now() - token.last_activity) > timezone.timedelta(hours=1):
            token.used = True
            token.save(update_fields=['used'])
            raise AuthenticationFailed('Expired token')

        token.last_activity = timezone.now()
        token.save(update_fields=['last_activity'])

        return (token.user, token)