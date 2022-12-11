import json
from datetime import datetime

from django.template.defaulttags import register

from .models import Measurement, Role, User, Reading


def get_or_create_role(name):
    try:
        role = Role.objects.get(name=name)
    except Role.DoesNotExist:
        role = Role(name=name)
        role.save()
    return(role)


def get_or_create_user(login):
    try:
        user = User.objects.get(login=login)
    except User.DoesNotExist:
        role = Role.objects.get(name="USER")
        user = User(login=login, role=role, )
        user.save()
    return(user)




def get_or_create_measurement(name, unit):
    measurement, created = Measurement.objects.get_or_create(
        name=name, unit=unit)
    return(measurement)




def create_reading(value: float, measure: Measurement, date: datetime, user: User):
    data = Reading(value=value, measurement=measure, time=date, user = user)
    data.save_and_smear_timestamp()
    return(data)


def get_last_measure(station, measurement):
    last_measure = Reading.objects.filter(
        station=station, measurement=measurement).latest('time')
    print(last_measure.time)
    print(datetime.now())
    return(last_measure.value)


def get_statistic(dictionary, key):
    if type(dictionary) == str:
        dictionary = json.loads(dictionary)
    if key is None:
        return None
    keys = [k.strip() for k in key.split(',')]
    return dictionary.get(keys[0]).get(keys[1])


'''
Filtro para formatear datos en los templates
'''


@ register.filter
def add_str(str1, str2):
    return str1 + str2
