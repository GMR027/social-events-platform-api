# Generated by Django 3.2.7 on 2021-10-03 04:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0011_auto_20211002_2235'),
    ]

    operations = [
        migrations.RenameField(
            model_name='eventuserregistration',
            old_name='covid_test_result',
            new_name='img_covid_test_result',
        ),
        migrations.RenameField(
            model_name='eventuserregistration',
            old_name='responsive_letter',
            new_name='img_signed_responsive_letter',
        ),
    ]