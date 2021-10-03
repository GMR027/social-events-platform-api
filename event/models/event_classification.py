from django.db import models
from common.models import MediumPicture
from common.tools import set_media_url, get_unique_slug

# Create your models here.

def event_pictures(instance, filename):
    return set_media_url("events/", filename)

class EventClassification(MediumPicture):
    title=models.CharField (
        max_length=64,
        null=False,
        blank=False
    )
    slug=models.SlugField (
        max_length=64,
        null=True,
        blank=True,
        unique=True
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug=get_unique_slug(
                self.title,
                EventClassification
            )
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name="Categoría del evento"
        verbose_name_plural="Categorías de los eventos"

    class JSONAPIMeta:
        resource_name="EventClassification"
