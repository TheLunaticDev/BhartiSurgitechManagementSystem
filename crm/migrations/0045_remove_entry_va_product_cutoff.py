# Generated by Django 5.1.1 on 2024-10-18 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0044_alter_entry_va'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='entry',
            name='va',
        ),
        migrations.AddField(
            model_name='product',
            name='cutoff',
            field=models.BigIntegerField(default=0, verbose_name='Cutoff(Incl. GST)'),
            preserve_default=False,
        ),
    ]
