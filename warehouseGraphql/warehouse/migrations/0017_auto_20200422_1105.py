# Generated by Django 3.0.5 on 2020-04-22 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('warehouse', '0016_tour_is_open'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='customer_id',
            field=models.CharField(max_length=10),
        ),
    ]
