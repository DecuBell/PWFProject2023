# Generated by Django 4.2.4 on 2023-08-11 15:34

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0009_alter_ads_expiration_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ads',
            name='expiration_date',
            field=models.DateField(default=datetime.datetime(2023, 8, 18, 15, 34, 2, 331560, tzinfo=datetime.timezone.utc)),
        ),
    ]
