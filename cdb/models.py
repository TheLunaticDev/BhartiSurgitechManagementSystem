from django.db import models

from crm.models import( 
    Area, Sector, Discipline, HospitalType,
)


class CDBEntry(models.Model):
    institute = models.CharField(max_length=200)
    area = models.ForeignKey(Area, on_delete=models.CASCADE)
    landmark = models.CharField(max_length=300)
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE)
    discipline = models.ForeignKey(Discipline, on_delete=models.CASCADE)
    hospital_type = models.ForeignKey(HospitalType, on_delete=models.CASCADE)

    def __str__(self):
        return self.institute

    class Meta:
        verbose_name_plural = 'CDB Entries'

        
class CDBAdministrator(models.Model):
    name = models.CharField(max_length=255)
    designation = models.CharField(max_length=255)
    email = models.EmailField(blank=True)
    phone_number = models.CharField(max_length=15)
    entry = models.ForeignKey(CDBEntry, on_delete=models.CASCADE, related_name='admins')

    class Meta:
        verbose_name_plural = 'CDB Admins'


class CDBDoctor(models.Model):
    name = models.CharField(max_length=255)
    speciality = models.CharField(max_length=255)
    designation = models.CharField(max_length=255)
    email = models.EmailField(blank=True)
    phone_number = models.CharField(max_length=15)
    entry = models.ForeignKey(CDBEntry, on_delete=models.CASCADE, related_name='doctors')

    class Meta:
        verbose_name_plural = 'CDB Doctors'
    

class CDBReference(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True)
    phone_number = models.CharField(max_length=15)
    entry = models.ForeignKey(CDBEntry, on_delete=models.CASCADE, related_name='references')

    class Meta:
        verbose_name_plural = 'CDB References'