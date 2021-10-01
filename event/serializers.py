from rest_framework_json_api.serializers import HyperlinkedModelSerializer
from rest_framework_json_api.relations import ResourceRelatedField
from event.models import (
    EventClassification,
    Event,
    EventPicture,
    Expositor,
    EventAgenda,
    EventUserRegistration
)

class EventClassificationSerializer(HyperlinkedModelSerializer):

    class Meta:
        model=EventClassification
        fields="__all__"


class EventSerializer(HyperlinkedModelSerializer):

    classification=ResourceRelatedField(queryset=EventClassification.objects)
    pictures=ResourceRelatedField(
        queryset=EventPicture.objects,
        many=True
    )
    agenda_items=ResourceRelatedField(
        queryset=EventAgenda.objects,
        many=True
    )

    included_serializers = {
        "classification": "event.serializers.EventClassificationSerializer",
        "pictures": "event.serializers.EventPictureSerializer",
        "agenda_items": "event.serializers.EventAgendaSerializer",
    }

    class Meta:
        model=Event
        fields="__all__"


class EventPictureSerializer(HyperlinkedModelSerializer):
    event=ResourceRelatedField(queryset=Event.objects)

    class Meta:
        model=EventPicture
        fields="__all__"


class EventAgendaSerializer(HyperlinkedModelSerializer):
    event=ResourceRelatedField(queryset=Event.objects)
    pictures=ResourceRelatedField(
        queryset=EventPicture.objects,
        many=True
    )
    expositor=ResourceRelatedField(queryset=Expositor.objects)

    included_serializers = {
        "event": "event.serializers.EventSerializer",
        "pictures": "event.serializers.EventPictureSerializer",
        "expositor": "event.serializers.ExpositorSerializer",
    }

    class Meta:
        model=EventAgenda
        fields="__all__"


class ExpositorSerializer(HyperlinkedModelSerializer):

    class Meta:
        model=Expositor
        fields="__all__"


class EventUserRegistrationSerializer(HyperlinkedModelSerializer):
    event=ResourceRelatedField(queryset=Event.objects)

    class Meta:
        model=EventUserRegistration
        fields="__all__"
