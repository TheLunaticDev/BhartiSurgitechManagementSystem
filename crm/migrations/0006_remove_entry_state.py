# Generated by Django 5.1.1 on 2024-09-24 08:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0005_alter_stage_win'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='entry',
            name='state',
        ),
    ]
