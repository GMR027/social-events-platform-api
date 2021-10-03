from django.db import models
from common.models import CommonFields
from common.tools import set_media_url
import uuid
from django_resized import ResizedImageField

def picture(instance, filename):
    return set_media_url( "CommonPicture", filename)

# Create your models here.

def event_pictures(instance, filename):
    return set_media_url("events/", filename)

class EventUserRegistration(CommonFields):
    event=models.ForeignKey(
        "event.Event",
        verbose_name="Evento",
        null=True,
        blank=False,
        on_delete=models.CASCADE
    )
    check_in_complete=models.BooleanField (
        verbose_name="Check in completo?",
        blank=False,
        default=False
    )
    first_name=models.CharField (
        max_length=32,
        null=False,
        blank=False
    )
    last_name=models.CharField (
        max_length=32,
        null=False,
        blank=False
    )
    zone=models.CharField (
        max_length=32,
        null=True,
        blank=True
    )
    city=models.CharField (
        max_length=32,
        null=False,
        blank=False
    )
    email=models.EmailField(
        null=False,
        blank=False
    )
    phone=models.CharField (
        max_length=10,
        null=True,
        blank=True
    )
    img_covid_test_result=ResizedImageField (
        null=False,
        blank=False,
        size=[1920, 1920],
        quality=90,
        upload_to=picture
    )
    img_signed_responsive_letter=ResizedImageField (
        null=False,
        blank=False,
        size=[1920, 1920],
        quality=90,
        upload_to=picture
    )
    emergency_phone=models.CharField (
        max_length=10,
        null=True,
        blank=True
    )
    identifier=models.UUIDField(
        default=uuid.uuid4,
        null=False,
        blank=False
    )

    def __str__(self):
        return self.first_name

    class Meta:
        verbose_name = "Registro de usuario al evento"
        verbose_name_plural = "Registros de usuarios al evento"
        unique_together = ('email', 'event',)

    class JSONAPIMeta:
        resource_name = "EventUserRegistration"
