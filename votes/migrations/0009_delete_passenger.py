# Generated by Django 2.0.2 on 2018-09-23 23:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('votes', '0008_passenger'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Passenger',
        ),
    ]