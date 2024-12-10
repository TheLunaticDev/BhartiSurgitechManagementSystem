from django.urls import path
from . import views

urlpatterns = [
    path('', views.demo_index_view, name='demo_index_view'),
    path('add/<int:entry_id>/', views.demo_add_get_form, name='demo_add_entry'),
    path('add/new/entry', views.demo_add_new_entry, name='demo_add_new_entry'),
    path('list/entry/', views.demo_load_entry_list_for_user, name='demo_load_entry_list_for_user'),
]