from django.db import models
from common.models import MediumPicture
from common.tools import set_media_url, get_unique_slug
from django_resized import ResizedImageField

# Create your models here.

def event_pictures(instance, filename):
    return set_media_url("events/", filename)

class Event(MediumPicture):
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
    classification=models.ForeignKey(
        "event.EventClassification",
        verbose_name="Clasificacion",
        null=False,
        blank=False,
        on_delete=models.CASCADE
    )
    private=models.BooleanField(
        verbose_name="Evento privado",
        blank=False,
        default=False
    )
    check_in_pin=models.CharField (
        verbose_name="Pin de 4 digitos para el Check in",
        max_length=4,
        null=False,
        blank=False
    )
    code=models.CharField (
        verbose_name="Codigo del evento de 4 digitos",
        max_length=4,
        null=True,
        blank=True
    )
    img_logo=ResizedImageField(
        verbose_name="Logo",
        null=True,
        blank=False,
        size=[256, 128],
        quality=100,
        upload_to=event_pictures,
        help_text="Logo del evento"
    )
    img_cover=ResizedImageField(
        verbose_name="Imágen Cover",
        null=True,
        blank=True,
        size=[1920, 1080],
        quality=90,
        upload_to=event_pictures,
        help_text="Imágen Cover del evento"
    )
    short_description=models.CharField(
        verbose_name="Descripción corta del evento",
        max_length=90,
        null=True,
        blank=True,
        help_text="Descripción corta (90 carácteres)"
    )
    start_date=models.DateField(
        null=False,
        blank=False,
        verbose_name="Fecha de inicio del evento"
    )
    end_date=models.DateField(
        null=False,
        blank=False,
        verbose_name="Fecha de fin del evento"
    )
    city=models.CharField (
        max_length=32,
        null=False,
        blank=False
    )
    address=models.CharField(
        verbose_name="Dirección del evento",
        max_length=256,
        null=False,
        blank=False
    )
    pictures=models.ManyToManyField(
        "event.EventPicture",
        related_name="event_pictures",
        verbose_name="Fotos",
        blank=True,
        help_text="Fotos del evento"
    )
    agenda_items=models.ManyToManyField(
        "event.EventAgenda",
        related_name="event_agenda",
        verbose_name="Elementos de agenda",
        blank=True,
        help_text="Exposiciones del evento"
    )
    map=ResizedImageField(
        verbose_name="Mapa",
        null=True,
        blank=True,
        size=[1920, 1920],
        quality=90,
        upload_to=event_pictures,
        help_text="Mapa del evento"
    )
    responsive_letter=ResizedImageField (
        null=True,
        blank=True,
        size=[1920, 1920],
        quality=90,
        upload_to=event_pictures
    )
    img_badge=ResizedImageField(
        verbose_name="Imágen para fondo del gafete",
        null=True,
        blank=True,
        size=[512, 512],
        quality=90,
        upload_to=event_pictures,
        help_text="Imágen para fondo del gafete"
    )
    video_live_link=models.URLField(
        verbose_name="Link del video en vivo",
        null=True,
        blank=True
    )
    facebook_link=models.URLField(
        verbose_name="Facebook del Evento",
        max_length=256,
        null=True,
        blank=True,
        help_text="Link del Facebook del Evento"
    )
    twitter_link=models.URLField(
        verbose_name="Twitter del Evento",
        null=True,
        blank=True,
        help_text="Link del Twitter del Evento"
    )
    instagram_link=models.URLField(
        verbose_name="Instagram del Evento",
        null=True,
        blank=True,
        help_text="Link del Instagram del Evento"
    )
    youtube_link=models.URLField(
        verbose_name="Youtube del Evento",
        null=True,
        blank=True,
        help_text="Link del Youtube del Evento"
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug=get_unique_slug(
                self.title,
                Event
            )
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name="Evento"
        verbose_name_plural="Eventos"

    class JSONAPIMeta:
        resource_name="Event"
