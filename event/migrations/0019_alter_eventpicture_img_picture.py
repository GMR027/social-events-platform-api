# Generated by Django 3.2.7 on 2021-10-05 00:03

import common.models.picture
from django.db import migrations
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0018_alter_event_img_cover'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventpicture',
            name='img_picture',
            field=django_resized.forms.ResizedImageField(blank=True, crop=None, force_format='JPEG', keep_meta=True, null=True, quality=85, size=[1080, 1080], upload_to=common.models.picture.picture),
        ),
    ]