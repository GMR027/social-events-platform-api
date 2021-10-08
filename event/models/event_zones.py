from django.db import models
from common.models import CommonFields

# Create your models here.

class Zone(CommonFields):
    zone=models.CharField (
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

    def __str__(self):
        return self.zone

    class Meta:
        verbose_name="Zona"
        verbose_name_plural="Zonas"

    class JSONAPIMeta:
        resource_name="Zone"
