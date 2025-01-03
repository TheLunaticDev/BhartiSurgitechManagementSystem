from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='tp_index_view'),
    path('manager/', views.manager_index_view_initial, name='tp_manager_index_view_initial'),
    path('manager/<int:subordinate_id>', views.manager_index_view_for_subordinate, name='tp_manager_index_view_for_subordinate'),
    path('update/<int:entry_id>/<str:field_name>', views.update_field, name='update_field'),
    path('edit/<int:entry_id>/<str:field_name>', views.edit_field, name='edit_field'),
    path('entry/add/crm', views.add_entry_from_crm, name='tp_add_entry_from_crm'),
    path('entry/add/cdb', views.add_entry_from_cdb, name='tp_add_entry_from_cdb'),
    path('popover-content/<int:entry_id>/', views.tp_popover_content, name='tp_popover_content'),
    path('toggle/not_visited/<int:entry_id>/', views.tp_toggle_not_visited, name="tp_toggle_not_visited"),
]