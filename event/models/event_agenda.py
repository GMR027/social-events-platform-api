from django.contrib.gis.db import models
from common.models import MediumPicture
from common.tools import set_media_url
from django_resized import ResizedImageField

# Create your models here.

def event_pictures(instance, filename):
    return set_media_url("events/", filename)

class EventAgenda(MediumPicture):
    title=models.CharField (
        max_length=64,
        null=False,
        blank=False
    )
    event = models.ForeignKey(
        "event.Event",
        verbose_name="Evento",
        null=True,
        blank=False,
        on_delete=models.CASCADE
    )
    expositor=models.ForeignKey (
        "event.Expositor",
        verbose_name="Expositor",
        null=True,
        blank=False,
        on_delete = models.SET_NULL
    )
    date=models.DateField(
        null=False,
        blank=False,
        verbose_name="Fecha"
    )
    starting_time=models.TimeField(
        null=False,
        blank=False,
        verbose_name="Inicio de exposicion"
    )
    ending_time=models.TimeField(
        null=False,
        blank=False,
        verbose_name="Inicio de exposicion"
    )
    map=ResizedImageField(
        verbose_name="Mapa",
        null=True,
        blank=True,
        size=[512, 512],
        quality=90,
        upload_to=event_pictures,
        help_text="Mapa de la exposicion"
    )
    video_live_link=models.URLField(
        verbose_name="Link del video en vivo",
        null=True,
        blank=True
    )
    pictures=models.ManyToManyField(
        "event.EventPicture",
        related_name="event_agenda_pictures",
        verbose_name="Fotos de la exposicion",
        blank=True,
        help_text="Fotos de la exposicion"
    )

    def __str__(self):
        return "{} - {}".format(
            self.title,
            self.event.title
        )

    class Meta:
        verbose_name="Agenda"
        verbose_name_plural="Agenda"

    class JSONAPIMeta:
        resource_name="EventAgenda"
