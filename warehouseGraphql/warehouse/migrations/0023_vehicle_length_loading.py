# Generated by Django 3.0.5 on 2020-04-27 09:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('warehouse', '0022_null'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehicle',
            name='length_loading',
            field=models.IntegerField(default=100),
            preserve_default=False,
        ),
    ]
