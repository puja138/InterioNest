# Generated by Django 5.2.1 on 2025-06-25 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_product_is_offer'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=15)),
                ('address', models.TextField()),
                ('product_name', models.CharField(max_length=100)),
                ('quantity', models.PositiveIntegerField()),
                ('order_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
