# Generated by Django 5.1.1 on 2024-10-17 04:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0033_alter_entry_expected'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='color',
            field=models.CharField(max_length=7, null=True),
        ),
    ]
