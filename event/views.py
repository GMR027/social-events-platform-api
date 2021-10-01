from rest_framework.viewsets import ModelViewSet
from event.models import (
    EventClassification,
    Event,
    EventPicture,
    Expositor,
    EventAgenda,
    EventUserRegistration
)
from event.serializers import (
    EventClassificationSerializer,
    EventSerializer,
    EventAgendaSerializer,
    EventPictureSerializer,
    EventUserRegistrationSerializer,
    ExpositorSerializer
)

# Create your views here.

class EventClassificationViewSet(ModelViewSet):
    queryset=EventClassification.objects.all()
    serializer_class=EventClassificationSerializer
    filter_fields=("enabled",)
    search_fields=("slug", "title", "description")
    ordering=( "id", )


class EventViewSet(ModelViewSet):
    queryset=Event.objects.all()
    serializer_class=EventSerializer
    filter_fields=(
        "enabled",
        "classification",
        "private"
    )
    search_fields=("slug", "title", "short_description", "description")
    ordering=( "id", )


class EventPictureViewSet(ModelViewSet):
    queryset=EventPicture.objects.all()
    serializer_class=EventPictureSerializer
    filter_fields=("enabled", "event")
    search_fields=("slug", "title")
    ordering=( "id", )


class ExpositorViewSet(ModelViewSet):
    queryset=Expositor.objects.all()
    serializer_class=ExpositorSerializer
    filter_fields=("enabled",)
    search_fields=("title", "short_description", "description")
    ordering=( "id", )


class EventAgendaViewSet(ModelViewSet):
    queryset=EventAgenda.objects.all()
    serializer_class=EventAgendaSerializer
    filter_fields=("enabled", "event", "date")
    search_fields=("title", "description")
    ordering=( "id", )


class EventUserRegistrationViewSet(ModelViewSet):
    queryset=EventUserRegistration.objects.all()
    serializer_class=EventUserRegistrationSerializer
    filter_fields=("event", "zone", "city", "check_in_complete")
    search_fields=("first_name", "last_name", "identifier", "email", "phone")
    ordering=( "id", )
