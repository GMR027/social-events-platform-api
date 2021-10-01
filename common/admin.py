from django.contrib import admin
from common.models import (
  Country,
  State,
  City,
  Sprint,
  ChangeLog
)

# Register your models here.

class CountryAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'code',
        'enabled',
    ]
    search_fields = ('name','code')
    list_filter = ('enabled',)
    readonly_fields=(
        'version',
        'order'
    )
admin.site.register(Country, CountryAdmin)

class StateAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'code',
        'country',
        'enabled'
    ]
    search_fields = ('name','country',)
    list_filter = ('enabled','country',)
    readonly_fields=(
        'version',
        'order'
    )
admin.site.register(State, StateAdmin)

class CityAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'state',
        'enabled'
    ]
    search_fields = ('name','state',)
    list_filter = ('enabled','state','state__country',)
    readonly_fields=(
        'version',
        'order'
    )
admin.site.register(City, CityAdmin)

class SprintAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'date_start',
        'date_end'
    ]
    search_fields = ('name',)
    readonly_fields=(
        'version',
        'order'
    )
admin.site.register(Sprint, SprintAdmin)

class ChangeLogAdmin(admin.ModelAdmin):
    list_display = [
        'task_name',
        'type',
        'hours',
        'user'
    ]
    search_fields = ('task_name',)
    list_filter = ('user', 'type')
    readonly_fields=(
        'version',
        'order'
    )
admin.site.register(ChangeLog, ChangeLogAdmin)
