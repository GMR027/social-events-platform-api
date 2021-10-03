# Generated by Django 3.2.7 on 2021-10-01 06:43

from django.db import migrations
import django_resized.forms
import event.models.event
import event.models.event_agenda


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0009_auto_20211001_0406'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='map',
            field=django_resized.forms.ResizedImageField(blank=True, crop=None, force_format='JPEG', help_text='Mapa del evento', keep_meta=True, null=True, quality=90, size=[1920, 1080], upload_to=event.models.event.event_pictures, verbose_name='Mapa'),
        ),
        migrations.AlterField(
            model_name='eventagenda',
            name='map',
            field=django_resized.forms.ResizedImageField(blank=True, crop=None, force_format='JPEG', help_text='Mapa de la exposicion', keep_meta=True, null=True, quality=90, size=[1920, 1080], upload_to=event.models.event_agenda.event_pictures, verbose_name='Mapa'),
        ),
    ]
