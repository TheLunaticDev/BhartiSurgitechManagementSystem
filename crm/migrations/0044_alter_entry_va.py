# Generated by Django 5.1.1 on 2024-10-18 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0043_alter_productentry_options_product_va_alter_entry_va_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='va',
            field=models.DecimalField(decimal_places=1, editable=False, max_digits=3, null=True),
        ),
    ]