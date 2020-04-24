from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('polyglotte/', include('bible.urls')),
    path('admin/', admin.site.urls),
]
