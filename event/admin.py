from django.contrib import admin
from django.http import HttpResponse
import csv
from event.models import (
    EventClassification,
    Event,
    EventPicture,
    Expositor,
    EventAgenda,
    EventUserRegistration,
    Zone
)

# Register your models here.

# EXPORT AS CSV
class ExportCsvMixin:
    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)
        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])
        return response
     
    export_as_csv.short_description = "Exportar seleccionados a Excel"

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
        "private",
        "city"
    ]
    search_fields=("slug", "title", "short_description", "description")
    list_filter=(
        "enabled",
        "classification",
        "private",
        "city"
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
        "ending_time",
        "location"
    ]
    search_fields=("title", "description")
    list_filter=("enabled", "event", "date", "location")
    readonly_fields=(
        "href",
        "version"
    )

admin.site.register(EventAgenda, EventAgendaAdmin)


class EventUserRegistrationAdmin(admin.ModelAdmin, ExportCsvMixin):
    actions = ["export_as_csv"]
    list_display=[
        "first_name",
        "last_name",
        "event",
        "identifier",
        "check_in_complete",
        "phone"
    ]
    search_fields=("first_name", "last_name", "identifier", "email", "phone")
    list_filter=("event", "zone", "check_in_complete")
    readonly_fields=(
        "version",
        "identifier",
        "order"
    )

admin.site.register(EventUserRegistration, EventUserRegistrationAdmin)


class ZoneAdmin(admin.ModelAdmin):
    list_display=[
        "zone",
        "event"
    ]
    search_fields=("zone",)
    list_filter=("enabled", "event")
    readonly_fields=(
        "order",
        "version"
    )

admin.site.register(Zone, ZoneAdmin)
