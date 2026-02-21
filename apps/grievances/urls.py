

from rest_framework.routers import DefaultRouter

from apps.grievances.views.citizen_views import GrievanceViewSet
from apps.grievances.views.officer_views import OfficerGrievanceViewSet
from apps.grievances.views.admin_views import AdminGrievanceViewSet

router = DefaultRouter()

router.register(r'citizen', GrievanceViewSet, basename='citizen-grievance')
router.register(r'officer', OfficerGrievanceViewSet, basename='officer-grievance')
router.register(r'admin', AdminGrievanceViewSet, basename='admin-grievance')

urlpatterns = router.urls
