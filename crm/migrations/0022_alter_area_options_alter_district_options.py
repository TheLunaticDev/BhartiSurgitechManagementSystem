# Generated by Django 5.1.1 on 2024-10-04 03:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0021_alter_district_unique_together_district_code_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='area',
            options={'ordering': ['district']},
        ),
        migrations.AlterModelOptions(
            name='district',
            options={'ordering': ['state']},
        ),
    ]
