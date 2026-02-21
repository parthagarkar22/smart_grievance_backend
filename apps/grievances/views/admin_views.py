

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework import status

from apps.grievances.models import Grievance
from apps.grievances.serializers import (
    GrievanceSerializer,
    GrievanceStatusUpdateSerializer,
)

# 🔔 Notification Celery task
from apps.notifications.tasks import create_notification


class AdminGrievanceViewSet(ModelViewSet):
    """
    Admin:
    - View all grievances
    - Update grievance status
    - Delete grievances
    """

    queryset = Grievance.objects.all()
    permission_classes = [IsAdminUser]

    def get_serializer_class(self):
        if self.action in ["partial_update", "update"]:
            return GrievanceStatusUpdateSerializer
        return GrievanceSerializer

    # 🔥 Runs AFTER status update
    def perform_update(self, serializer):
        grievance = serializer.save()  # ✅ DB updated

        # 🔔 Notify citizen asynchronously
        create_notification.delay(
            grievance.user.id,
            f"Your grievance #{grievance.id} status changed to {grievance.status}"
        )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(
            {"message": "Grievance deleted successfully"},
            status=status.HTTP_200_OK
        )
