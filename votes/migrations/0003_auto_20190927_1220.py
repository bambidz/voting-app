# Generated by Django 2.0.7 on 2019-09-27 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('votes', '0002_auto_20190927_1212'),
    ]

    operations = [
        migrations.AlterField(
            model_name='response',
            name='v_response',
            field=models.IntegerField(blank=True, default=1),
        ),
    ]
