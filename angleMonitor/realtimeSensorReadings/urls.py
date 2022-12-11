from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import *

urlpatterns = [


    path('historical/', HistoricalView.as_view(), name='historical'),
    path('logout/', LogoutView.as_view(), name='logout'),

]
