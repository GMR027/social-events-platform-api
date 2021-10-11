from django.db import models
from common.models import RegularPicture
from common.tools import set_media_url

# Create your models here.

def event_pictures(instance, filename):
    return set_media_url("events/", filename)

class EventPicture(RegularPicture):
    event = models.ForeignKey(
        "event.Event",
        verbose_name="Evento",
        null=True,
        blank=False,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return "{} - {}".format(
            self.title or "-",
            self.event.title
        )

    def save(self, *args, **kwargs):
        if not self.title:
            self.title="image"

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Foto del evento"
        verbose_name_plural = "Fotos de evento"

    class JSONAPIMeta:
        resource_name = "EventPicture"
