import binascii, os, bcrypt, base64
from django.conf import settings
from django.utils.text import slugify
from enum import Enum
from django.core.files import File
import os, re, json


class Currency(Enum):
    MXN = "MXN"
    USD = "USD"


def get_random_mame( size=None ):
	return binascii.hexlify(os.urandom(size)).decode()


def set_media_url( path, filename ):
	ext = filename.split('.')[-1]
	renamedfile = '{}/{}.{}'.format (
        path,
        get_random_mame(18),
        ext
    )
	return renamedfile


def get_media_url(image_name):
    if image_name:
        return "{}/{}/{}".format(settings.HOST, settings.MEDIA_ROOT, image_name)


def get_cypher_password(password):
    if password:
        password = bcrypt.hashpw(bytes(password, 'utf8'), bcrypt.gensalt(14)).decode("utf-8")
    return password


def base64_to_file(picture, dir):
    if not picture:
        return None
    try:
        os.stat(settings.MEDIA_ROOT)
    except:
        os.mkdir(settings.MEDIA_ROOT)

    try:
        os.stat(settings.MEDIA_ROOT + '/' + dir)
    except:
        os.mkdir(settings.MEDIA_ROOT + '/' + dir)

    if picture.find(";base64,") < 0 and picture.find("/") < 0:
        return None

    ext = picture.split(';base64,')[0]
    ext = ext.split('/')[-1]
    picture = picture.split(';base64,')[1]
    picture_name = set_media_url(dir,'picture_profile.' + ext )
    print('write', settings.MEDIA_ROOT + '/' + picture_name)
    with open(settings.MEDIA_ROOT + '/' + picture_name, "wb") as fh:
        fh.write(base64.decodebytes( bytes(picture,'utf8') ))
    return picture_name

def save_base64_picture(request):
    dir = 'common'
    try:
        dir = '{0}'.format(json.loads(request.body.decode('utf-8'))['data']['type']).lower() # Improve this for modles using common picture model
        pass
    except:
        pass
    print('>>>>> dir', dir)
    for i in request.data:
        if len(re.findall(r'img',i)) > 0:
            picture = base64_to_file( request.data[i], 'events' ) # Fix!!!!
            path = os.path.join(settings.BASE_DIR, settings.MEDIA_ROOT + '/' + picture)
            print('>>>>> path', path)
            picture = open(path, 'rb')
            request.data[i] = File(picture)
            os.remove(path)
    return request


def get_unique_slug(string, Model):
    slug = slugify(string)
    unique_slug = slug
    num = 1
    while Model.objects.filter(slug=unique_slug).exists():
        unique_slug = '{}-{}'.format(slug, num)
        num += 1
    return unique_slug


# # Utilities
# import base64

#
# from io import BytesIO
#
# import jwt
# from PIL import Image
#
# from django.core.cache import cache
# from django.core.exceptions import ObjectDoesNotExist
# from django.core.validators import RegexValidator
# from django.shortcuts import get_object_or_404
# from django.utils.html import strip_tags
#
# import requests
# from django.conf import settings
#
# from rest_framework import status
#
# #
# # regex used in model validators
# #
# from rest_framework.response import Response
#
# REGEX_VALIDATORS = {
# 	'PASSWORD': RegexValidator(**{
# 		'regex': (r'^(?=.*\d)(?=.*[\u0021-\u002b\u003c-\u0040])(?=.*[A-Z])(?=.*[a-z])\S{8,20}$'),  # noqa
# 		'message': (
# 			'The password should have one lowercase, one uppercase, '
# 			'one number and one special character.'
# 		)
# 	}),
# 	'URL': RegexValidator(**{
# 		'regex': r'^[A-Za-z0-9_]+$',
# 		'message': (
# 			'The URL should have only letters, numbers and underscores '
# 		)
# 	}),
# }
#
# def clear_cache():
# 	return cache._cache.flush_all()
#
#

#
# def set_media_url(path,filename):
# 	ext = filename.split('.')[-1]
# 	renamedfile = '{}{}.{}'.format(path,get_random_mame(6), ext)
# 	return renamedfile
#
# def get_error(errors):
# 	error = ""
# 	for i in errors:
# 		error = str(i) + " - " + str(errors[i])
# 	return error
#
# def object_does_not_exist(object):
#     return {
#         'data': {
#             "success": False,
#             "error": "Object ['" + str(object) + "'] does not exist."
#         },
#         'status': status.HTTP_404_NOT_FOUND
#     }
#
# def try_to_get_object_or_404(Model,id,object_str):
#     try:
#         return get_object_or_404(Model, id=id)
#     except ObjectDoesNotExist:
#         return {
#             'data': {
#                 "success": False,
#                 "error": "Object ['" + str(object_str) + "'] does not exist."
#             },
#             'status': status.HTTP_404_NOT_FOUND
#         }
#

# # Function to validete courrent session
# def validate_jwt(request):
#     if 'HTTP_TOKEN' not in request.META:
#         return False
#     token = request.META['HTTP_TOKEN']
#     try:
#         token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
#     except:
#         return False
#     if token:
#         return token
#     else:
#         return False
#
# def clean_html_text(html):
# 	strip_text = strip_tags(html).replace('&nbsp;', ' ')
# 	return strip_text
