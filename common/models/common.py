from django.db import models

class CommonFields(models.Model):
    enabled=models.BooleanField (
        verbose_name="Registro habilitado",
        blank=False,
        default=True,
        help_text="Define si este registro estará habilitado"
    )
    order = models.PositiveIntegerField(
        verbose_name="índice de ordenamiento",
        null=True,
        blank=True,
        default=0,
        help_text="Índice númerico de ordenamiento de este registro"
    )
    created=models.DateTimeField (
        auto_now_add=True,
        null=False
    )
    modified=models.DateTimeField (
        auto_now=True
    )
    version=models.PositiveIntegerField (
        default=1,
        blank=False,
        null=False
    )
    
    def save(self, *args, **kwargs):
        self.version=self.version + 1
        super().save(*args, **kwargs)

    class Meta:
        abstract=True
