# Generated by Django 5.1.4 on 2025-05-01 05:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0029_alter_catalogue_pdf_file'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='catalogue',
            name='pdf_file',
        ),
        migrations.AlterField(
            model_name='cataloguepage',
            name='catalogue',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='catalogue_pages', to='companies.catalogue'),
        ),
    ]
