from django.urls import path
from .views import execute_natural_query

urlpatterns = [
    path('execute_natural/', execute_natural_query, name='execute_natural_query'),
]

