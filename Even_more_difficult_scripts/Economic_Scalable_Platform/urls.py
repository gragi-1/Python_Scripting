# ecommerce/urls.py
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),  # Add Django's auth URLs
    path('products/', include('products.urls')),  # Add your products app URLs
    # Add your own URLs here
]