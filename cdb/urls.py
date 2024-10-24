from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='cdb_index_view'),
    path('popover-content/<int:entry_id>', views.cdb_popover_content, name='cdb_popover_content'),
]