# Generated by Django 3.2.7 on 2021-10-10 04:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0022_auto_20211010_0424'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='city',
            field=models.CharField(max_length=32, verbose_name='Ciudad'),
        ),
    ]