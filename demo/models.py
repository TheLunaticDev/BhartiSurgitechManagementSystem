from django.db import models
from django.contrib.auth.models import User
from crm.models import Area, Product, Entry

class DemoEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    institute = models.CharField(max_length=200)
    area = models.ForeignKey(Area, on_delete=models.CASCADE)
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE, null=True)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()


    class Meta:
        verbose_name = "Demo Entries"

    def __str__(self):
        return self.name


class DemoProductEntry(models.Model):
    demo_entry = models.ForeignKey(DemoEntry, on_delete=models.CASCADE, related_name='products')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


class DemoEntryNotes(models.Model):
    text = models.TextField(max_length=2000)
    demo_entry = models.ForeignKey(DemoEntry, on_delete=models.CASCADE, related_name='notes')
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Demo Notes"

    def __str__(self):
        return "Note on " + self.demo_entry + " by " + self.owner