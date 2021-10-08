from rest_framework.viewsets import ModelViewSet, GenericViewSet
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework_simplejwt.views import TokenObtainPairView
import json
from rest_framework.response import Response
from django.conf import settings
from rest_framework import mixins, status
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from django.core.mail import EmailMultiAlternatives
from common.mixins import (
    CustomCreate,
    CustomUpdate
)


from event.models import (
    EventClassification,
    Event,
    EventPicture,
    Expositor,
    EventAgenda,
    EventUserRegistration,
    Zone
)
from event.serializers import (
    EventClassificationSerializer,
    EventSerializer,
    EventAgendaSerializer,
    EventPictureSerializer,
    EventUserRegistrationSerializer,
    ExpositorSerializer,
    ZoneSerializer
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
        "private",
        "slug",
        "city"
    )
    search_fields=(
        "slug",
        "title",
        "short_description",
        "description",
        "city"
    )
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


class EventZoneViewSet(ModelViewSet):
    queryset=Zone.objects.all()
    serializer_class=ZoneSerializer
    filter_fields=("enabled", "event")
    search_fields=("zone",)
    ordering=( "id", )


class EventUserRegistrationViewSet(
        CustomCreate,
        CustomUpdate,
        mixins.ListModelMixin,
        mixins.RetrieveModelMixin,
        mixins.DestroyModelMixin,
        GenericViewSet
    ):
    queryset=EventUserRegistration.objects.all()
    serializer_class=EventUserRegistrationSerializer
    filter_fields=("event", "zone", "city", "check_in_complete", "identifier")
    search_fields=("first_name", "last_name", "identifier", "email", "phone")
    ordering=( "id", )


@method_decorator(csrf_exempt, name="dispatch")
class UserCheckIn(APIView):
    def post(self, request, *args, **kwargs):
        body_unicode=request.body.decode("utf-8")
        body = json.loads(body_unicode)
        get_object_or_404(
            Event,
            enabled=True,
            check_in_pin=body["data"]["attributes"]["pin"]
        )
        user = get_object_or_404(
            EventUserRegistration,
            enabled = True,
            identifier=body["data"]["attributes"]["identifier"]
        )
        user.check_in_complete=True
        user.save()
        return Response( data = {
            "success": True
        }, status = status.HTTP_200_OK )


@method_decorator(csrf_exempt, name="dispatch")
class RetrieveBadge(APIView):
    def post(self, request, *args, **kwargs):
        body_unicode=request.body.decode("utf-8")
        body = json.loads(body_unicode)
        user = get_object_or_404(
            EventUserRegistration,
            enabled=True,
            email=body["data"]["attributes"]["email"],
            event=body["data"]["attributes"]["event"]
        )
        event = get_object_or_404(
            Event,
            enabled=True,
            id=body["data"]["attributes"]["event"]
        )
        subject = "Gafete para evento"
        from_email = "Evtfy"
        to = user.email
        text_content = "Aqui esta su gafete: {}badge/{}".format(
            settings.WEB_APP_URL,
            user.identifier
        )
        html_content = """
            <img src={}media/{} />
            <br/>
            <h2>{}, hemos encontrado su gafete para el evento {}!</h2>
            <p>
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
        return Response( data = {
            "success": True
        }, status = status.HTTP_200_OK )
