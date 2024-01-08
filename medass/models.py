from django.db import models
from django.contrib.auth.models import User

from _config.settings.base import MEDIA_ROOT
from _config.utils import uuid_filepath

class MedassData(models.Model):

    # Override delete() to delete connected csv file
    def delete(self, *args, **kargs):
        import os
        if self.csv_data:
            os.remove(os.path.join(MEDIA_ROOT, self.csv_data.path))
        super(MedassData, self).delete(*args, **kargs)

    user = models.ForeignKey(User, verbose_name="username", on_delete=models.PROTECT)
    date_created = models.DateTimeField("date created", auto_now=False, auto_now_add=True)
    csv_data = models.FileField("csv data file", upload_to=uuid_filepath, max_length=None, null=False)
    note = models.TextField("user notes")