



from django.utils import timezone
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from apps.grievances.models import Grievance
from apps.grievances.serializers import (
    GrievanceSerializer,
    GrievanceStatusUpdateSerializer,
)

from apps.notifications.tasks import create_notification


class OfficerGrievanceViewSet(ModelViewSet):
    """
    Officer:
    - View grievances of own department
    - Update status of own department grievances
    """

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        # 🔐 Safety check
        if not user.is_staff or not user.department:
            return Grievance.objects.none()

        return Grievance.objects.filter(department__iexact=user.department)

    def get_serializer_class(self):
        if self.action in ["partial_update", "update"]:
            return GrievanceStatusUpdateSerializer

        return GrievanceSerializer

    # 🔥 IMPORTANT: Assign officer when updating
    def perform_update(self, serializer):
        grievance = serializer.save()

        # ✅ ASSIGN OFFICER IF NOT ALREADY ASSIGNED
        if grievance.assigned_to is None:
            grievance.assigned_to = self.request.user

        # ✅ If resolved, set resolved_at
        if grievance.status == "resolved":
            grievance.resolved_at = timezone.now()

        grievance.save()

        # 🔔 Notify citizen
        create_notification.delay(
            grievance.user.id,
            f"Your grievance #{grievance.id} status changed to {grievance.status}"
        )

    def destroy(self, request, *args, **kwargs):
        raise PermissionDenied("Officers cannot delete grievances")
