from realtimeSensorReadings.models import Measurement, Role, User, Reading
from django.contrib.auth.models import User as AuthUser
from datetime import datetime, timedelta
from django.db.models import Max
import random

from . import settings
import random
from datetime import datetime, timedelta

from django.contrib.auth.models import User as AuthUser
from django.db.models import Max

from realtimeSensorReadings.models import Measurement, Role, User, Reading
from . import settings


def register_users():
    registered_count = 0
    registering_count = 0
    error_count = 0

    print('Utils: Registering users...')

    with open(settings.BASE_DIR / "users.pwd", "r") as users_file:
        lines = users_file.readlines()
        for line in lines:
            [login, passwd] = line.split(':')
            login = login.strip()
            passwd = passwd.strip()
            try:
                role, created = Role.objects.get_or_create(
                    name="USER", active=True)
                userDB, userCreated = User.objects.get_or_create(login=login, defaults={
                    'email': login + '@uniandes.edu.co',
                    'password': passwd,
                    'role': role,
                })
                userAuth = AuthUser.objects.get(username=login)
                registered_count += 1
            except AuthUser.DoesNotExist:
                AuthUser.objects.create_user(
                    login, login + '@uniandes.edu.co', passwd)
                registering_count += 1
            except Exception as e:
                print(f'Error registering u: {login}. Error: {e}')
                error_count += 1
        print('Utils: Users registered.')
        print(
            f'Utils: Already users: {registered_count}, \
                 Registered users: {registering_count}, \
                     Error use rs: {error_count}, Total success: \
                         {registered_count+ registering_count}'
        )



def saveMeasure(user: str, date: datetime, variable: str, measure: float):
    from realtimeSensorReadings.views import create_reading, get_or_create_measurement, get_or_create_user
    try:
        user_obj = get_or_create_user(user)
        unit = '°'
        variable_obj = get_or_create_measurement(variable, unit)
        create_reading(measure, variable_obj, date, user_obj)
    except Exception as e:
        print("ERROR saving measure: ", e)








def generateData(quantity: int = 500000):
    print("Starting generation of {} data...".format(quantity))

    data_len = Reading.objects.count()

    print("Data in database:", data_len)

    if data_len > quantity:
        print("Mock data already generated.")
        return

    measure1, created = Measurement.objects.get_or_create(
        name="kneeAngle", unit="°")
    measure2, created = Measurement.objects.get_or_create(
        name="ankleAngle", unit="°")

    role, created = Role.objects.get_or_create(name="TEST")

    user1, created = User.objects.get_or_create(login="userMock1", role=role)

    data_per_day = 20000
    initial_date = '20/06/2021'
    interval = ((24*60*60*1000)/data_per_day) // 1

    print("Init date: ", initial_date)
    print("Data per day: ", data_per_day)
    print("Interval (milliseconds):", interval)

    measures = Measurement.objects.all()
    print("Total measures:", len(measures))

    if data_len > 0:
        cd_query = Reading.objects.aggregate(Max("time"))
        current_date = cd_query["time__max"]
        current_date = current_date + timedelta(hours=1)
    else:
        current_date = datetime.strptime(initial_date, "%d/%m/%Y")

    count = data_len if data_len != None else 0

    while count <= quantity:

        rand_measure = random.randint(0, len(measures)-1)
        measure = measures[rand_measure]
        data = (random.random()*40)

        Reading.objects.create(measurement=measure,
                                    value=data, time=current_date, user = user1)
        print("Data created:", count, current_date.timestamp())
        count += 1
        current_date += timedelta(milliseconds=interval)

    print("Finished. Total data:", count, "Last date:", current_date)
