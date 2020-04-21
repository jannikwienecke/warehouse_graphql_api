# Generated by Django 2.1.4 on 2020-04-20 19:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('warehouse', '0007_auto_20200420_2120'),
    ]

    operations = [
        migrations.AlterField(
            model_name='row',
            name='number_stock_positions',
            field=models.IntegerField(default=None),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='row',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='warehouse.Product'),
        ),
    ]