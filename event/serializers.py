from rest_framework_json_api.serializers import HyperlinkedModelSerializer
from rest_framework_json_api.relations import ResourceRelatedField
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
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

    included_serializers = {
        "event": "event.serializers.EventSerializer"
    }

    class Meta:
        model=EventUserRegistration
        fields="__all__"
    
    def create(self, validated_data):
        user = EventUserRegistration()
        for i in validated_data:
            setattr(user, i, validated_data[i])
        event=validated_data["event"]
        subject = "Registro exitoso al evento"
        from_email = "Long Event"
        to = user.email
        text_content = "Registro exitoso al evento, aqui esta su gafete: {}badge/{}".format(
            settings.WEB_APP_URL,
            user.identifier
        )
        html_content = """
                <img src={}{} />
                <br/>
                <h2>{}, se ha registrado exitosamente al evento {}!</h2>
                <p>
                    Si necesita acceder a su gafete virtual, por favor de click en el
                    siguiente enlace en cualquier momento:
                    <a href="{}badge/{}">Click Aqui.</a>
                </p><br/>
                <span>Gracias!</span>
                <br/>
            """.format(
                settings.API_URL,
                event.img_logo,
                user.first_name,
                event.title,
                settings.WEB_APP_URL,
                user.identifier
            )
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        user.save()
        return user
