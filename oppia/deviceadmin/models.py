from django.contrib.auth.models import User
from django.db import models

# Create your models here.
# import the AbstractDevice class to inherit from
from gcm.models import AbstractDevice


class UserDevice(AbstractDevice):
    user = models.ForeignKey(User)
    model_name = models.TextField(blank=True, null=True, default=None)
