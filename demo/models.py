from django.db import models
from django.contrib.auth.models import User
from crm.models import Area, Product

class DemoEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    institute = models.CharField(max_length=200)
    area = models.ForeignKey(Area, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()


    class Meta:
        verbose_name = "Demo Entries"

    def __str__(self):
        return self.name


class DemoEntryNotes(models.Model):
    text = models.TextField(max_length=2000)
    demo_entry = models.ForeignKey(DemoEntry, on_delete=models.CASCADE, related_name='notes')
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Demo Notes"

    def __str__(self):
        return "Note on " + self.demo_entry + " by " + self.owner