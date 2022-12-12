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

