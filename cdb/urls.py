from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='cdb_index_view'),
]