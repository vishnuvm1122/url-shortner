from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),          # ✅ correct
    path('', include('shortner.urls')),  # ✅ correct
    path('accounts/', include('users.urls')),
]