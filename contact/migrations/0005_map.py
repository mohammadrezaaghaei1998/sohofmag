# Generated by Django 5.1.4 on 2025-05-23 22:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0004_faq'),
    ]

    operations = [
        migrations.CreateModel(
            name='Map',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('iframe', models.TextField(verbose_name='Google Maps iframe')),
            ],
        ),
    ]
