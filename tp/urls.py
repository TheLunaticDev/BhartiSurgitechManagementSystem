from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='tp_index_view'),
    path('update/<int:entry_id>/<str:field_name>', views.update_field, name='update_field'),
    path('edit/<int:entry_id>/<str:field_name>', views.edit_field, name='edit_field'),
    path('entry/add/crm', views.add_entry_from_crm, name='tp_add_entry_from_crm'),
    path('entry/add/cdb', views.add_entry_from_cdb, name='tp_add_entry_from_cdb'),
    path('entry/edit/', views.edit_view, name='tp_edit_view'),
    path('popover-content/<int:entry_id>/', views.tp_popover_content, name='tp_popover_content'),
]