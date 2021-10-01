from django.contrib import admin
from event.models import (
    EventClassification,
    Event,
    EventPicture,
    Expositor,
    EventAgenda,
    EventUserRegistration
)

# Register your models here.

class EventClassificationAdmin(admin.ModelAdmin):
    list_display=[
        "slug",
        "title",
        "enabled",
    ]
    search_fields=("slug", "title", "description")
    list_filter=("enabled",)
    readonly_fields=(
        "href",
        "version"
    )

admin.site.register(EventClassification, EventClassificationAdmin)


class EventAdmin(admin.ModelAdmin):
    list_display=[
        "slug",
        "title",
        "classification",
        "private"
    ]
    search_fields=("slug", "title", "short_description", "description")
    list_filter=(
        "enabled",
        "classification",
        "private"
    )
    readonly_fields=(
        "href",
        "version"
    )

admin.site.register(Event, EventAdmin)


class EventPictureAdmin(admin.ModelAdmin):
    list_display=[
        "title",
        "event",
        "enabled",
    ]
    search_fields=("slug", "title")
    list_filter=("enabled", "event")
    readonly_fields=(
        "href",
        "version"
    )

admin.site.register(EventPicture, EventPictureAdmin)


class ExpositorAdmin(admin.ModelAdmin):
    list_display=[
        "title",
    ]
    search_fields=("title", "short_description", "description")
    list_filter=("enabled",)
    readonly_fields=(
        "href",
        "version"
    )

admin.site.register(Expositor, ExpositorAdmin)


class EventAgendaAdmin(admin.ModelAdmin):
    list_display=[
        "title",
        "event",
        "expositor",
        "date",
        "starting_time",
        "ending_time"
    ]
    search_fields=("title", "description")
    list_filter=("enabled", "event", "date")
    readonly_fields=(
        "href",
        "version"
    )

admin.site.register(EventAgenda, EventAgendaAdmin)


class EventUserRegistrationAdmin(admin.ModelAdmin):
    list_display=[
        "first_name",
        "last_name",
        "event",
        "identifier",
        "check_in_complete",
        "city",
        "phone"
    ]
    search_fields=("first_name", "last_name", "identifier", "email", "phone")
    list_filter=("event", "zone", "city", "check_in_complete")
    readonly_fields=(
        "version",
        "identifier",
        "order"
    )

admin.site.register(EventUserRegistration, EventUserRegistrationAdmin)
