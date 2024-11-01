from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='product_list'),
    path('filter/category/<int:category_id>', views.filter_by_category, name='product_list_filter_by_category'),
    path('filter/query/', views.product_list_search, name='product_list_search'),
    path('configs/<int:product_id>', views.get_product_configurations, name='get_product_configurations'),
]
