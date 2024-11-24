from django.db import models
from django.contrib.auth.models import User
from crm.models import (
    Area, Sector, Discipline, HospitalType,
    Stage, Product, ProductEntry
)


class PurposeType(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name


class Purpose(models.Model):
    name = models.CharField(max_length=100)
    purpose_type = models.ForeignKey(PurposeType, related_name='purposes', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ['name', 'purpose_type']


class TPEntry(models.Model):
    CRM = 'CRM'
    CDB = 'CDB'
    NA = 'NA'
    TYPE_CHOICE = [
        (CRM, 'CRM'),
        (CDB, 'CDB'),
        (NA, 'NA'),
    ]
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tp_entries')
    type = models.CharField(max_length=5, choices=TYPE_CHOICE, blank=True)
    link = models.PositiveBigIntegerField(blank=True, null=True)
    institute = models.CharField(max_length=200)
    area = models.ForeignKey(Area, on_delete=models.CASCADE)
    landmark = models.CharField(max_length=300, blank=True)
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE)
    discipline = models.ForeignKey(Discipline, on_delete=models.CASCADE)
    hospital_type = models.ForeignKey(HospitalType, on_delete=models.CASCADE)
    stage = models.ForeignKey(Stage, null=True, blank=True, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, blank=True)
    schedule = models.DateTimeField(blank=True, null=True)
    purpose = models.ForeignKey(Purpose, on_delete=models.CASCADE, null=True, blank=True)
    not_visited = models.BooleanField(default=False)

    def __str__(self):
        return self.institute

    def location(self):
        return f"{self.area} | {self.area.district.name} | {self.area.district.state.name}"

    def product_list(self):
        return " | ".join([str(product) for product in self.products.all()])

    class Meta:
        verbose_name_plural = 'TP Entries'