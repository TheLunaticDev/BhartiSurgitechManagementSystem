from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='cdb_index_view'),
    path('cdbentry/', views.cdbentry_list, name='cdbentry_list'),
    path('cdbentry/select/', views.cdbentry_list_for_select_view, name='cdbentry_list_for_select_view'),
    path('select/', views.select_view, name='cdb_select_view'),
    path('popover-content/<int:entry_id>', views.cdb_popover_content, name='cdb_popover_content'),
    path('cdbentry/visited/toggle/<int:entry_id>', views.cdb_toggle_visited, name='cdb_toggle_visited'),
]