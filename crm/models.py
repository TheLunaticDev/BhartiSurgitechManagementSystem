import datetime
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from base.models import Setting, Brochure


class Sector(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

        
class Discipline(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

        
class HospitalType(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name


class State(models.Model):
    name = models.CharField(max_length=150, unique=True)
    code = models.CharField(max_length=2, unique=True)
    
    def __str__(self):
        return self.name

class District(models.Model):
    name = models.CharField(max_length=150)
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='districts')

    def __str__(self):
        return self.name
    
    class Meta:
        unique_together = ['name', 'state']
        ordering = ['state']
    

class Area(models.Model):
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='areas')
    name = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['district']


class StageGroup(models.Model):
    name = models.CharField(max_length=100, unique=True)
    order = models.IntegerField()
    text_color = models.CharField(max_length=7, default="#ffffff")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['order']

class Stage(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=500)
    win = models.PositiveIntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100),
        ]
    )
    group = models.ForeignKey(StageGroup, related_name='stages', on_delete=models.SET_NULL, null=True, blank=True)
    order = models.IntegerField(
        default=0, 
        help_text='Set the order for this stage.'
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['order']


class Category(models.Model):
    name = models.CharField(max_length=150, unique=True)
    text_color = models.CharField(max_length=7, default="#ffffff")
    order = models.IntegerField(
        default=0,
        help_text='Set the order for this product category.',
    )

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['order']
        verbose_name_plural = 'Categories'


class Product(models.Model):
    limiter = 100000
    name = models.CharField(max_length=150, unique=True)
    quoted_price = models.PositiveBigIntegerField(verbose_name='Quoted Price')
    cutoff = models.PositiveBigIntegerField(verbose_name='Cutoff (Incl. GST)')
    purchase_price = models.PositiveBigIntegerField(verbose_name='Purchase Price')
    dealer_price = models.PositiveBigIntegerField(verbose_name='Sub Dealer Price')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    brochure = models.ForeignKey(Brochure, blank=True, null=True, on_delete=models.SET_NULL, related_name='related_products')

    def va_percentage(self):
        if self.purchase_price == 0:
            return "UNDEFINED"
        return str(round(((self.cutoff - self.purchase_price) / self.purchase_price) * 100)) + '%'
    
    def gross_va(self):
        return round((self.cutoff - self.purchase_price) / self.limiter, 1)
    
    def net_va(self):
        return round(self.gross_va() / 2, 1)

    def incentive(self):
        return round((self.cutoff - self.purchase_price) * (5 / 100))

    def employee_incentive(self):
        return round(self.incentive() * float(Setting.objects.get(key='EMPLOYEE_INCENTIVE').value))

    def manager_incentive(self):
        return round(self.incentive() * float(Setting.objects.get(key='MANAGER_INCENTIVE').value))

    def va(self):
        return self.net_va()

    def __str__(self):
        return self.name

    va_percentage.short_description = "VA%"

    class Meta:
        ordering = ['category', 'name']


class Configuration(models.Model):
    name = models.CharField(max_length=150)
    quantity = models.IntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='configurations')

    
class Entry(models.Model):
    EXPECTED_CHOICES = [
        ('-2', 'N/A'),
        ('-1', 'BEYOND'),
        ('0', 'JAN'),
        ('1', 'FEB'),
        ('2', 'MAR'),
        ('3', 'APR'),
        ('4', 'MAY'),
        ('5', 'JUN'),
        ('6', 'JUL'),
        ('7', 'AUG'),
        ('8', 'SEP'),
        ('11', 'OCT'),
        ('9', 'NOV'),
        ('10', 'DEC'),
    ]
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='entry')
    institute = models.CharField(max_length=200)
    area = models.ForeignKey(Area, on_delete=models.CASCADE)
    landmark = models.CharField(max_length=300, blank=True)
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE)
    discipline = models.ForeignKey(Discipline, on_delete=models.CASCADE)
    hospital_type = models.ForeignKey(HospitalType, on_delete=models.CASCADE)
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE)
    expected = models.CharField(max_length=2, choices=EXPECTED_CHOICES)
    products = models.ManyToManyField(Product, through='ProductEntry', related_name='entries')
    notes = models.CharField(max_length=2000, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    has_been_executed = models.BooleanField(default=False)

    def yet_to_be_contacted(self):
        if self.stage.group and self.stage.group.name == 'BIRD':
            if self.created_on < timezone.now() - datetime.timedelta(days=2):
                return True
        return False

    def va(self):
        total_value = sum(product_entry.count * product_entry.product.va() for product_entry in self.product_entries.all())
        return total_value

    def execution_va(self):
        total_value = 0
        for product_entry in self.product_entries.all():
            if product_entry.has_execution:
                if product_entry.execution_count and product_entry.execution_va:
                    total_value += (product_entry.execution_count * product_entry.execution_va)
                elif product_entry.execution_count and product_entry.execution_va == None:
                    total_value += (product_entry.execution_count * product_entry.product.va())
                elif product_entry.execution_count == None and product_entry.execution_va:
                    total_value += (product_entry.count * product_entry.execution_va)
                else:
                    total_value += (product_entry.count * product_entry.product.va())
        return total_value

    def time_since_creation(self):
        current_time = timezone.now()
        time_diff = current_time - self.created_on
        if time_diff < datetime.timedelta(days=1):
            return "Today"
        elif time_diff < datetime.timedelta(days=7):
            days_ago = time_diff.days
            return f'{days_ago} day{'s' if days_ago > 1 else ''} ago'
        elif time_diff < datetime.timedelta(days=365):
            months_ago = time_diff.days // 30
            if months_ago < 1:
                weeks_ago = time_diff.days // 7
                return f'{weeks_ago} week{'s' if weeks_ago > 1 else ''} ago'
            return f'{months_ago} month{'s' if months_ago > 1 else ''} ago'
        else:
            years_ago = time_diff.days // 365
            return f'{years_ago} year{'s' if years_ago > 1 else ''} ago'
        
    def __str__(self):
        return self.institute

    class Meta:
        verbose_name_plural = 'Entries'
        ordering = ['stage']


class ProductEntry(models.Model):
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE, related_name='product_entries')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_entries')
    count = models.PositiveIntegerField(default=1)
    has_execution = models.BooleanField(default=False, blank=True)
    execution_count = models.PositiveIntegerField(default=0, blank=True, null=True)
    execution_va = models.DecimalField(default=0.0, max_digits=3, decimal_places=1, blank=True, null=True)

    def __str__(self):
        return f'{self.product.name} - {self.count}'

    class Meta:
        verbose_name_plural = 'ProductEntries'

        
class Doctor(models.Model):
    name = models.CharField(max_length=255)
    speciality = models.CharField(max_length=255)
    designation = models.CharField(max_length=255)
    email = models.EmailField(blank=True)
    phone_number = models.CharField(max_length=15)
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE, related_name='doctors')

    def __str__(self):
        return self.name


class Administrator(models.Model):
    name = models.CharField(max_length=255)
    designation = models.CharField(max_length=255)
    email = models.EmailField(blank=True)
    phone_number = models.CharField(max_length=15)
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE, related_name='admins')

    def __str__(self):
        return self.name


class Reference(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True)
    phone_number = models.CharField(max_length=15)
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE, related_name='references')

    def __str__(self):
        return self.name

