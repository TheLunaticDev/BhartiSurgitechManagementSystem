from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name="crm_index_view"),
    path('edit/', views.edit_view, name="crm_edit_view"),
    path('manage/init/', views.manager_index_view_initial, name="crm_manager_index_view_initial"),
    path('manager/', views.manager_index_view, name="crm_manager_index_view"),
    path('manager/<int:subordinate_id>/', views.manager_index_view, name="crm_manager_index_view_with_id"),
    path('manager/edit/', views.manager_edit_view, name="crm_manager_edit_view"),
    path('manager/edit/<int:subordinate_id>/', views.manager_edit_view, name="crm_manager_edit_view_with_id"),
    path('district-autocomplete/', views.DistrictAutoComplete.as_view(), name="district-autocomplete"),
    path('doctor-autocomplete/', views.DoctorAutoComplete.as_view(), name='doctor-autocomplete'),
    path('popover-content/<int:entry_id>', views.popover_content, name='popover_content')
]
