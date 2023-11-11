# utlis.py
import os
from uuid import uuid4
from django.utils import timezone

# Encrypting file name
def uuid_filepath(instance, filename):
    app_name = instance.__class__._meta.app_label
    model_name = instance.__class__.__name__.lower()
    uuid_name = uuid4().hex
    extension = os.path.splitext(filename)[-1].lower()
    return '/'.join([
        app_name,
        model_name,
        uuid_name + extension,
    ])

# Generating email verification token
from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six

class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (six.text_type(user.pk) + six.text_type(timestamp)) + six.text_type(user.is_active)

account_activation_token = AccountActivationTokenGenerator()

#