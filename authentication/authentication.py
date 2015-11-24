from rest_framework.authentication import TokenAuthentication
from rest_framework import exceptions
from django.conf import settings
import datetime, pytz


class ExpiringTokenAuthentication(TokenAuthentication):
	def authenticate_credentials(self, key):
		try:
			token = self.model.objects.get(key=key)
		except self.model.DoesNotExist:
			raise exceptions.AuthenticationFailed('Invalid token : ' + key.__str__())

		if not token.user.is_active:
			raise exceptions.AuthenticationFailed('User inactive or deleted')

		# This is required for the time comparison
		utc_now = datetime.datetime.utcnow()
		utc_now = utc_now.replace(tzinfo=pytz.utc)

		if token.created < utc_now - settings.EXPIRATION_DELTA:
			raise exceptions.AuthenticationFailed('Token has expired')

		return token.user, token
