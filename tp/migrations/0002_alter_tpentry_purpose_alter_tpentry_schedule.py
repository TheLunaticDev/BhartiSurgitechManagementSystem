# Generated by Django 5.1.1 on 2024-10-25 08:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tpentry',
            name='purpose',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tp.purpose'),
        ),
        migrations.AlterField(
            model_name='tpentry',
            name='schedule',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
