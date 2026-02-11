from django.contrib import admin
from django.urls import path, include   # ✅ include added
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Admin site
    path('admin/', admin.site.urls),

    # API routes from your app
    path('api/', include('main.urls')),  # ✅ include main app urls here
]

# MEDIA FILES
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

