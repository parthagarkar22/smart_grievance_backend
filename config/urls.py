
from django.contrib import admin
from django.urls import path, include
from apps.accounts.views import create_admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("apps.accounts.urls")),
   path('api/grievances/', include('apps.grievances.urls')),
   path("api/dashboard/", include("apps.dashboard.urls")),
   path("api/feedback/", include("apps.feedback.urls")),
   path("api/notifications/", include("apps.notifications.urls")),
   path('create-admin/', create_admin),
   path('api/', include('apps.grievances.urls')),

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



