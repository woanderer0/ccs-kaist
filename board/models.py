from django.db import models
from django.contrib.auth.models import User

class Note(models.Model):
    user = models.ForeignKey(User, verbose_name="username", on_delete=models.PROTECT)
    date_created = models.DateTimeField("date created", auto_now=False, auto_now_add=True)
    content = models.TextField("content on note", null=False)