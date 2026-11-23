


# from rest_framework.routers import DefaultRouter
# from django.conf import settings
# from django.conf.urls.static import static
# from django.urls import path

# from apps.grievances.views.citizen_views import GrievanceViewSet
# from apps.grievances.views.officer_views import OfficerGrievanceViewSet
# from apps.grievances.views.admin_views import (
#     AdminGrievanceViewSet,
#     MonthlyReportView
# )

# router = DefaultRouter()

# router.register(r'citizen', GrievanceViewSet, basename='citizen-grievance')
# router.register(r'officer', OfficerGrievanceViewSet, basename='officer-grievance')
# router.register(r'admin', AdminGrievanceViewSet, basename='admin-grievance')

# urlpatterns = [
#     path("admin/monthly-report/", MonthlyReportView.as_view(), name="monthly-report"),
# ]

# urlpatterns += router.urls


# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from apps.grievances.views.citizen_views import GrievanceViewSet
from apps.grievances.views.officer_views import OfficerGrievanceViewSet
from apps.grievances.views.admin_views import (
    AdminGrievanceViewSet,
    MonthlyReportView,
    EscalatedComplaintsAPIView,     # 🆕 NEW
    TakeActionOnOfficerAPIView      # 🆕 NEW
)

router = DefaultRouter()

router.register(r'citizen', GrievanceViewSet, basename='citizen-grievance')
router.register(r'officer', OfficerGrievanceViewSet, basename='officer-grievance')
router.register(r'admin', AdminGrievanceViewSet, basename='admin-grievance')

urlpatterns = [
    # 📊 Existing Report API
    path(
        "admin/monthly-report/",
        MonthlyReportView.as_view(),
        name="monthly-report"
    ),

    # 🚨 NEW: Escalated Complaints API
    path(
        "admin/escalated-complaints/",
        EscalatedComplaintsAPIView.as_view(),
        name="escalated-complaints"
    ),

    # ⚠️ NEW: Take Action on Officer API
    path(
        "admin/take-action/<int:grievance_id>/",
        TakeActionOnOfficerAPIView.as_view(),
        name="take-action-on-officer"
    ),
]

urlpatterns += router.urls


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)