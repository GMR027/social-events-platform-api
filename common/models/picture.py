from django.db import models
from tinymce.models import HTMLField
from common.models import CommonFields
from common.tools import set_media_url
from django_resized import ResizedImageField

def picture(instance, filename):
    return set_media_url( "CommonPicture", filename)

class BasePicture(CommonFields):
    title=models.CharField (
        max_length=64,
        null=True,
        blank=True
    )
    description=HTMLField (
        null=True,
        blank=True,
        default="Descripción"
    )
    href=models.URLField (
        null=True,
        blank=True
    )

    class Meta:
        abstract=True

class SmallPicture(BasePicture):
    img_picture=ResizedImageField (
        null=True,
        blank=True,
        size=[256, 256],
        quality=85,
        upload_to=picture
    )

    class Meta:
        abstract=True

class MediumPicture(BasePicture):
    img_picture=ResizedImageField (
        null=True,
        blank=True,
        size=[512, 512],
        quality=85,
        upload_to=picture
    )

    class Meta:
        abstract=True

class RegularPicture(BasePicture):
    img_picture=ResizedImageField (
        null=True,
        blank=True,
        size=[1080, 1080],
        quality=85,
        upload_to=picture
    )

    class Meta:
        abstract=True

class LargePicture(BasePicture):
    img_picture=ResizedImageField (
        null=True,
        blank=True,
        size=[1920, 1920],
        quality=85,
        upload_to=picture
    )

    class Meta:
        abstract=True
