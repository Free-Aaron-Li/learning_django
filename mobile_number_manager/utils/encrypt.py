import hashlib

from django.conf import settings


def sha256(data_string):
    obj = hashlib.sha256(settings.SECRET_KEY.encode('utf-8'))
    obj.update(data_string.encode('utf-8'))
    return obj.hexdigest()
