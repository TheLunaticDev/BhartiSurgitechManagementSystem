# Generated by Django 5.1.1 on 2024-10-19 05:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0051_alter_product_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='expected',
            field=models.CharField(choices=[('-2', 'N/A'), ('-1', 'BEYOND'), ('0', 'JAN'), ('1', 'FEB'), ('2', 'MAR'), ('3', 'APR'), ('4', 'MAY'), ('5', 'JUN'), ('6', 'JUL'), ('7', 'AUG'), ('8', 'SEP'), ('11', 'OCT'), ('9', 'NOV'), ('10', 'DEC')], max_length=2),
        ),
    ]
