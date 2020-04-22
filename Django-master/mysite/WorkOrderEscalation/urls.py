from django.urls import path
from . import views
from django.urls import path
from . import views


urlpatterns = [
    path('', views.WorkOrderEscalate, name='WorkOrderEscalate'),
]