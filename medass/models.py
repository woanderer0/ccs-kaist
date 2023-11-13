from django.db import models
from django.contrib.auth.models import User

from _config.utils import uuid_filepath

class MedassData(models.Model):
    user = models.ForeignKey(User, verbose_name="username", on_delete=models.PROTECT)
    date_created = models.DateTimeField("date created", auto_now=False, auto_now_add=True)
    csv_data = models.FileField("csv data file", upload_to=uuid_filepath, max_length=None, null=False)