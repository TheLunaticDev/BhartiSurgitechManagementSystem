from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name="crm_index_view"),
    path('manage/init/', views.manager_index_view_initial, name="crm_manager_index_view_initial"),
    path('manager/', views.manager_index_view, name="crm_manager_index_view"),
    path('manager/<int:subordinate_id>/', views.manager_index_view, name="crm_manager_index_view_with_id"),
    path('district-autocomplete/', views.DistrictAutoComplete.as_view(), name="district-autocomplete"),
    path('doctor-autocomplete/', views.DoctorAutoComplete.as_view(), name='doctor-autocomplete'),
    path('popover-content/<int:entry_id>', views.crm_popover_content, name='crm_popover_content'),
    path('add_to_tp/', views.crm_select_view, name='crm_select_view'),
    path('filter/districts/', views.filter_districts, name='filter_districts'),
    path('filter/areas/', views.filter_areas, name='filter_areas'),
    path('add/area', views.add_new_area, name='add_new_area'),
    path('manager/add/entry/', views.add_new_entry_as_manager, name='add_new_entry_as_manager'),
]
