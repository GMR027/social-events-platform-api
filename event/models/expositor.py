from django.db import models
from common.models import MediumPicture
from common.tools import set_media_url

# Create your models here.

def event_pictures(instance, filename):
    return set_media_url("expositors/", filename)

class Expositor(MediumPicture):
    title=models.CharField (
        verbose_name="Nombre del expositor",
        max_length=64,
        null=False,
        blank=False
    )
    hidden=models.BooleanField (
        verbose_name="Ocultar expositor",
        blank=False,
        default=False,
        help_text="Define si la/el expositor(a) sera visible o no"
    )
    short_description=models.CharField(
        verbose_name="Descripción corta del expositor",
        max_length=90,
        null=True,
        blank=True,
        help_text="Descripción corta (90 carácteres)"
    )
    link=models.URLField(
        verbose_name="Link del expositor",
        max_length=256,
        null=True,
        blank=True,
        help_text="Link del expositor"
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name="Expositor"
        verbose_name_plural="Expositores"

    class JSONAPIMeta:
        resource_name="Expositor"
