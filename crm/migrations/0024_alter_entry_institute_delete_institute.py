# Generated by Django 5.1.1 on 2024-10-04 04:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0023_alter_district_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='institute',
            field=models.CharField(max_length=200),
        ),
        migrations.DeleteModel(
            name='Institute',
        ),
    ]
