# Generated by Django 2.0 on 2018-08-10 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0003_sensor_showname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='access_token',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
