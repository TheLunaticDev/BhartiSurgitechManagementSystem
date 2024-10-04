from django.contrib import admin
from django.urls import include, path
from debug_toolbar.toolbar import debug_toolbar_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include("django.contrib.auth.urls")),
    path('', include('crm.urls')),
    path('sys/admin/', include('sysadmin.urls')),
] + debug_toolbar_urls()
