# Generated by Django 3.0.5 on 2020-04-22 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('warehouse', '0017_auto_20200422_1105'),
    ]

    operations = [
        migrations.AddField(
            model_name='withdrawal',
            name='quantiy',
            field=models.IntegerField(default=10),
            preserve_default=False,
        ),
    ]
