from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
import datetime

class Command(BaseCommand):
	help = 'Removes user which has not been activated for certain amount of time'

	def handle(self, *args, **options):
		userlist = User.objects.filter(is_active=False)

		for user in userlist:
			inactive_time = datetime.datetime.today() - user.date_joined
			expiration_time = datetime.timedelta(days=1)

			if inactive_time > expiration_time:
				print(f'Remove `{user.username}`, inactivated for {inactive_time}...', end='')
				try:
					user.delete()
					print('done')
				except Exception as e:
					print('failed')
					print(f'Failed to remove user: {e}')