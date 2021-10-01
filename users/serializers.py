import uuid
from django.conf import settings
from rest_framework_json_api import serializers
from rest_framework_json_api.serializers import HyperlinkedModelSerializer
from rest_framework.validators import UniqueValidator
from rest_framework_json_api.relations import ResourceRelatedField
from django.contrib.auth.models import User, Group
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.core.mail import EmailMultiAlternatives
from users.models import UserAddress, UserProfile
from common.models import City
import re

# Create your serializers here.

class GroupSerializer(HyperlinkedModelSerializer):
  class Meta:
    model = Group
    fields = ['url', 'name']


class UserProfileSerializer(HyperlinkedModelSerializer):
    
    class Meta:
        model = UserProfile
        fields = '__all__'


class UserSerializer(HyperlinkedModelSerializer):
    groups = ResourceRelatedField (
        queryset = Group.objects,
        many = True,
        required = False
    )
    email = serializers.EmailField (
        required = True,
        validators = [
            UniqueValidator(queryset=User.objects.all())
        ]
    )
    included_serializers = {
        'groups': GroupSerializer
    }
    profile = serializers.SerializerMethodField()
    
    def get_profile(self, user):
        uri = str(self.context.get("request").build_absolute_uri())
        path = str(self.context.get("request").get_full_path())
        dns = uri.replace(path,'')
        profile = UserProfile.objects.filter(user=user.id)
        if len(profile) > 0:
            profile=profile[0]
            img=None
            if profile.img_picture is not None:
                img='{}/media/{}'.format(
                    dns,
                    str(profile.img_picture)
                )
            return {
                'newsletter': profile.newsletter,
                'promotions': profile.promotions,
                'img_picture': img,
                'biography': profile.biography,
                'owner_position': profile.owner_position,
                'owner_position_description': profile.owner_position_description,
                'owner_phone': profile.owner_phone,
                'owner_office_phone': profile.owner_office_phone,
                'owner_email': profile.owner_email,
                'owner_whatsapp': profile.owner_whatsapp,
                'owner_address': profile.owner_address
            }
        return None

    class Meta:
        model = User
        fields = [
            'url','username', 'email', 'last_login',
            'first_name', 'last_name', 'password',
            'is_superuser', 'groups', 'date_joined',
            'is_active', 'is_staff', 'profile'
        ]
        extra_kwargs = {
            'password': {
                'write_only': True,
                'required': False
            },
            'is_superuser': {
                'read_only': True
            },
            'is_staff': {
                'read_only': True
            },
            'is_active': {
                'read_only': True
            },
            'last_login': {
                'read_only': True
            },
            'date_joined': {
                'read_only': True
            }
        }

    def create(self, validated_data):
        user = User()
        for i in validated_data:
            setattr(user, i, validated_data[i])
        user.set_password(validated_data['password'])
        if len(re.findall(r'SN-', user.username)) > 0:
            user.is_active = True
            user.save()
            profile = UserProfile()
            profile.user = user
            profile.save()
            return user
        user.is_active = False
        token = uuid.uuid4()
        if settings.ENVIRONMENT != 'localhost':
            subject = 'Activa tu cuenta de Nedii'
            from_email = settings.EMAIL_HOST_USER
            to = user.email
            text_content = 'Para continuar, por favor activa tu cuenta de Nedii en el siguiente <a href=activate/>link.</a>'
            html_content = '''
                <h2>Bienvenido a Nedii {0}!</h2>
                <p>
                    Para continuar, por favor activa tu cuenta de Nedii con el siguiente
                    <a href="{1}activate/{2}">link.</a>
                </p>
                <span>El equipo de Nedii.</span>
                <br/>
            '''.format(
                user.first_name,
                settings.WEB_APP_URL,
                token
            )
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
        user.save()
        profile = UserProfile()
        profile.user = user
        profile.token = token
        profile.save()
        return user

    def update(self, instance, validated_data):
        for i in validated_data:
            setattr(instance, i, validated_data[i])
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])
        instance.save()
        return instance


class UserAddressSerializer(HyperlinkedModelSerializer):
    user = ResourceRelatedField (
        queryset = User.objects,
        required = False
    )
    city = ResourceRelatedField (
        queryset = City.objects,
        required = False
    )
    included_serializers = {
        'city': 'common.serializers.CitySerializer',
        'user': UserSerializer
    }

    class Meta:
        model = UserAddress
        fields = '__all__'
        extra_kwargs = {
            'user': {
                'read_only': True
            },
            'created': {
                'read_only': True
            },
            'modified': {
                'read_only': True
            }
        }

class UserLoginSerializer(
        HyperlinkedModelSerializer,
        TokenObtainPairSerializer
    ):
    access = serializers.SerializerMethodField()
    refresh = serializers.SerializerMethodField()

    def get_access(self, user):
        token = super().get_token(user).access_token
        token['admin'] = user.is_superuser
        token['user_agent'] = user.user_agent
        token['ip'] = user.remote_addr
        return str(token)

    def get_refresh(self, user):
        token = super().get_token(user)
        return str(token)

    class Meta:
        model = User
        exclude = (
            'is_staff',
            'password'
        )
        meta_fields = (
            'access',
            'refresh'
        )
