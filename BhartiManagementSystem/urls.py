from django.contrib import admin
from django.urls import include, path
from debug_toolbar.toolbar import debug_toolbar_urls
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include("django.contrib.auth.urls")),
    path('', include('crm.urls')),
    path('cdb/', include('cdb.urls')),
    path('demo/', include('demo.urls')),
    path('tp/', include('tp.urls')),
    path('sys/admin/', include('sysadmin.urls')),
    path('products/', include('productlist.urls')),
] + debug_toolbar_urls() + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
