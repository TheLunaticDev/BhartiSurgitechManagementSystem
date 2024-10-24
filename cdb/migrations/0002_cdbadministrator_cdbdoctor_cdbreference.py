# Generated by Django 5.1.1 on 2024-10-23 10:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cdb', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CDBAdministrator',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('designation', models.CharField(max_length=255)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('phone_number', models.CharField(max_length=15)),
                ('entry', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='admins', to='cdb.cdbentry')),
            ],
            options={
                'verbose_name_plural': 'CDB Admins',
            },
        ),
        migrations.CreateModel(
            name='CDBDoctor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('speciality', models.CharField(max_length=255)),
                ('designation', models.CharField(max_length=255)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('phone_number', models.CharField(max_length=15)),
                ('entry', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='doctors', to='cdb.cdbentry')),
            ],
            options={
                'verbose_name_plural': 'CDB Doctors',
            },
        ),
        migrations.CreateModel(
            name='CDBReference',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('phone_number', models.CharField(max_length=15)),
                ('entry', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='references', to='cdb.cdbentry')),
            ],
            options={
                'verbose_name_plural': 'CDB References',
            },
        ),
    ]
