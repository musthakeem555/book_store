# Generated by Django 4.2.3 on 2023-08-19 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0004_order_order_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='order_status',
        ),
        migrations.AddField(
            model_name='cartitem',
            name='order_status',
            field=models.CharField(default='order placed'),
        ),
    ]