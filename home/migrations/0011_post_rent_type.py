# Generated by Django 3.0.8 on 2020-11-29 05:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0010_auto_20201129_1113'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='rent_type',
            field=models.CharField(choices=[('Per Hour', 'Per Hour'), ('Per Day', 'Per Day'), ('Per Week', 'Per Week'), ('Per Month', 'Per Month'), ('Per Year', 'Per Year')], default='Per Hour', max_length=100),
        ),
    ]
