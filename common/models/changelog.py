from django.db import models
from common.models import CommonFields
from django.contrib.auth.models import User
from tinymce.models import HTMLField
from enum import Enum

class TaskType(Enum):
    BACK_END='back-end'
    FRONT_END='front-end'
    SERVER='server'
    CI_CD='ci-cd'
    DESIGN='design'
    DOCUMENTATION='documentation'
    CHANGE='change'
    IMRPOVEMENT='improvement'
    BUGFIX='bugfix'
    INTEGRATION='integration'

class Sprint(CommonFields):
    name=models.CharField(
        verbose_name="Sprint Name",
        max_length=256,
        null=False,
        blank=False
    )
    tasks=models.ManyToManyField(
        "common.ChangeLog",
        related_name="sprint_tasks",
        verbose_name="Tasks",
        blank=True
    )
    comments=HTMLField (
        null=True,
        blank=True
    )
    date_start=models.DateField (
        null=False
    )
    date_end=models.DateField (
        null=False
    )

    def __str__(self):
        return self.name

    class JSONAPIMeta:
        resource_name="Sprint"


class ChangeLog(CommonFields):
    task_name=models.CharField(
        verbose_name="Task Name",
        max_length=256,
        null=False,
        blank=False
    )
    type=models.CharField(
        null=True,
        blank=True,
        max_length=32,
        choices=[(i.value, i.value) for i in TaskType],
        default='front-end'
    )
    user=models.ForeignKey (
        User,
        null=False,
        blank=False,
        on_delete=models.CASCADE
    )
    hours=models.PositiveIntegerField(
        verbose_name="Development time (hours)",
        null=False,
        blank=False,
        default=1
    )
    description=HTMLField (
        null=False,
        blank=False,
        default="Task description, including git commit"
    )

    def __str__(self):
        return self.task_name

    class JSONAPIMeta:
        resource_name="ChangeLog"

