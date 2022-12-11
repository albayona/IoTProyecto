from django.db import models, IntegrityError
from django.db.models.fields import DateTimeField
from datetime import datetime, timedelta
from django.utils import timezone

USER_ROLE_ID = 1


class Role(models.Model):
    name = models.CharField(max_length=16, blank=False, unique=True)
    active = models.BooleanField(default=True)

    def str(self):
        return '{}'.format(self.name)


class User(models.Model):
    login = models.CharField(
        primary_key=True, max_length=50, unique=True, blank=False)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True)
    password = models.CharField(max_length=50, blank=True)
    email = models.EmailField(max_length=60, blank=True)
    role = models.ForeignKey(
        Role, on_delete=models.CASCADE, default=USER_ROLE_ID)
    active = models.BooleanField(default=True)

    def str(self):
        return '{}'.format(self.login)





class Measurement(models.Model):
    name = models.CharField(max_length=50, blank=False)
    unit = models.CharField(max_length=50, blank=False)
    max_value = models.FloatField(null=True, blank=True, default=None)
    min_value = models.FloatField(null=True, blank=True, default=None)
    active = active = models.BooleanField(default=True)

    def str(self):
        return '{} {}'.format(self.name, self.unit)




class Reading(models.Model):
    measurement = models.ForeignKey(Measurement, on_delete=models.CASCADE)
    value = models.FloatField(blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.DateTimeField(primary_key=True, default=timezone.now)

    def save(self, *args, **kwargs):
        self.save_and_smear_timestamp(*args, **kwargs)

    def save_and_smear_timestamp(self, *args, **kwargs):
        """Recursivly try to save by incrementing the timestamp on duplicate error"""
        try:
            super().save(*args, **kwargs)
        except IntegrityError as exception:
            # Only handle the error:
            #   psycopg2.errors.UniqueViolation: duplicate key value violates unique constraint "1_1_farms_sensorreading_pkey"
            #   DETAIL:  Key ("time")=(2020-10-01 22:33:52.507782+00) already exists.
            if all(k in exception.args[0] for k in ("Key", "time", "already exists")):
                # Increment the timestamp by 1 µs and try again
                self.time = self.time + timedelta(microseconds=1)
                self.save_and_smear_timestamp(*args, **kwargs)

    def str(self):
        return '{} {} {} {}'.format(self.user, self.time, self.ankle, self.knee)


