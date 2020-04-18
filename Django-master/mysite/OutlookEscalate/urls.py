from django.urls import path
from . import views
from django.urls import path
from . import views


urlpatterns = [
    path('', views.OutlookEsc, name='OutlookEsc'),
]