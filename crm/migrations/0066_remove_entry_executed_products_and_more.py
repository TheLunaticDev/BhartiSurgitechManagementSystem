# Generated by Django 5.1.1 on 2024-11-15 04:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0065_rename_quantity_executedproduct_count_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='entry',
            name='executed_products',
        ),
        migrations.AddField(
            model_name='productentry',
            name='is_selected',
            field=models.BooleanField(default=False),
        ),
        migrations.DeleteModel(
            name='ExecutedProduct',
        ),
    ]