from django.db import models
from django.contrib.auth.models import User


class Manager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    subordinates = models.ManyToManyField(User, related_name="managers")

    def __str__(self):
        return self.user.username