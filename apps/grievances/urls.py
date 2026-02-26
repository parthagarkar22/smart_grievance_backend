

from rest_framework.routers import DefaultRouter
from django.conf import settings
from apps.grievances.views.citizen_views import GrievanceViewSet
from apps.grievances.views.officer_views import OfficerGrievanceViewSet
from apps.grievances.views.admin_views import AdminGrievanceViewSet
from django.conf.urls.static import static

router = DefaultRouter()

router.register(r'citizen', GrievanceViewSet, basename='citizen-grievance')
router.register(r'officer', OfficerGrievanceViewSet, basename='officer-grievance')
router.register(r'admin', AdminGrievanceViewSet, basename='admin-grievance')

urlpatterns = router.urls

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)