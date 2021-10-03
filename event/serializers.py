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

    class Meta:
        model=EventUserRegistration
        fields="__all__"
    
    def create(self, validated_data):
        user = EventUserRegistration()
        for i in validated_data:
            print(i, validated_data[i])
            setattr(user, i, validated_data[i])
        subject = 'Registro exitoso al evento'
        from_email = settings.EMAIL_HOST_USER
        to = user.email
        text_content = 'Click'
        html_content = '''
                <h2>{0}, usted se ha registrado exitosamente al evento!</h2>
                <p>
                    Si necesita acceder a su codigo QR, por favor de click en el
                    siquiente enlace en cualquier momento:
                    <a href="{1}gafete/{2}">Click Aqui.</a>
                </p>
                <span>Gracias!</span>
                <br/>
            '''.format(
                user.first_name,
                settings.WEB_APP_URL,
                user.identifier
            )
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        user.save()
        return user
