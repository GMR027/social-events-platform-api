# Generated by Django 3.2.7 on 2021-10-07 05:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0019_alter_eventpicture_img_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='code',
            field=models.CharField(blank=True, max_length=4, null=True, verbose_name='Codigo del evento de 4 digitos'),
        ),
    ]