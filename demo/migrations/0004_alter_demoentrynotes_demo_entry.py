# Generated by Django 5.1.1 on 2024-12-09 05:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demo', '0003_remove_demoentry_notes_demoentrynotes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='demoentrynotes',
            name='demo_entry',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notes', to='demo.demoentry'),
        ),
    ]