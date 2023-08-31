# Generated by Django 4.2.3 on 2023-08-29 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_side', '0006_alter_order_status_order_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coupon_code', models.CharField(max_length=10, unique=True)),
                ('description', models.TextField()),
                ('minimum_amount', models.IntegerField()),
                ('discount_type', models.CharField(choices=[('amount', 'Amount'), ('percentage', 'Percentage')], max_length=20)),
                ('discount', models.DecimalField(decimal_places=2, max_digits=5)),
                ('valid_from', models.DateTimeField()),
                ('valid_to', models.DateTimeField()),
                ('active', models.BooleanField(default=True)),
            ],
        ),
    ]
