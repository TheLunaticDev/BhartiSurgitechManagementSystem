# Generated by Django 5.1.1 on 2024-11-21 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0069_alter_productentry_execution_count_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='stage',
            name='tracks_tp_link',
            field=models.BooleanField(default=False),
        ),
    ]
