import datetime
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator


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


class Stage(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=500)
    win = models.PositiveIntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100),
        ]
    )
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

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Categories'
    

class Product(models.Model):
    name = models.CharField(max_length=150, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')

    def __str__(self):
        return self.name


class Entry(models.Model):
    EXPECTED_CHOICES = [
        ('-2', 'NOT DEFINED'),
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
        ('9', 'NOV'),
        ('10', 'DEC'),
    ]
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='entry')
    institute = models.CharField(max_length=200)
    area = models.ForeignKey(Area, on_delete=models.CASCADE)
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE)
    expected = models.CharField(max_length=2, choices=EXPECTED_CHOICES)
    va = models.DecimalField(max_digits=3, decimal_places=1)
    products = models.ManyToManyField(Product)
    notes = models.CharField(max_length=2000, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    schedule_date = models.DateTimeField(blank=True, null=True)

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

