# Generated by Django 4.1.6 on 2023-03-24 16:58

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Bus', '0007_bookbus_user_alter_bookbus_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookbus',
            name='date',
            field=models.DateField(default=datetime.date(2023, 3, 24)),
        ),
    ]
