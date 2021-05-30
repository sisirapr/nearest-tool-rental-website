# Generated by Django 3.0.8 on 2020-11-26 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_pfilter'),
    ]

    operations = [
        migrations.CreateModel(
            name='AreaCoverage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('area_coverage', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='PriceRange',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price_range', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='RateRange',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate_range', models.CharField(max_length=100)),
            ],
        ),
        migrations.DeleteModel(
            name='PFilter',
        ),
    ]
