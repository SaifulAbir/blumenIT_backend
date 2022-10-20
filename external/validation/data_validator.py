from rest_framework import status
from rest_framework.response import Response
from rest_framework.validators import ValidationError


def check_dict_data_rise_error(key, kwargs_data=None, request_data=None, arrise=False):
    value = None
    if kwargs_data is not None:
        value = kwargs_data.get(key, None)
    if request_data is not None:
        value = request_data.get(key, None)
    if key and value is None and arrise:
        key = str(key).capitalize()
        key = key.split('_')
        message = " ".join(key) + ' is required'
        raise ValidationError(message)
    else:
        return value