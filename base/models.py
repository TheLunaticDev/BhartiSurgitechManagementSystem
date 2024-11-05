from django.db import models


class Setting(models.Model):
    key = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    value = models.TextField()

    def __str__(self):
        return f"{self.key}: {self.value}"


class Brochure(models.Model):
    identifying_name = models.CharField(max_length=255, unique=True)
    file = models.FileField()

    def __str__(self):
        return self.identifying_name