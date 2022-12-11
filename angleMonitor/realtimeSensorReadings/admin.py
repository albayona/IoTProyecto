from django.contrib import admin
from . models import  Measurement, Role, User, Reading

admin.site.register(Role)
admin.site.register(User)
admin.site.register(Measurement)
admin.site.register(Reading)
