# Generated by Django 5.1.1 on 2024-11-08 04:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0062_product_brochure'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='entry',
            name='schedule_date',
        ),
        migrations.AddField(
            model_name='entry',
            name='has_been_executed',
            field=models.BooleanField(default=False),
        ),
    ]
