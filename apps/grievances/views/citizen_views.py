



from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser

from apps.grievances.models import Grievance
from apps.grievances.serializers import GrievanceSerializer

from apps.grievances.tasks import run_ai_detection
from apps.notifications.tasks import create_notification


class GrievanceViewSet(ModelViewSet):
    serializer_class = GrievanceSerializer
    queryset = Grievance.objects.all()   # ✅ REQUIRED for router
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def get_queryset(self): 
        # Show only logged-in user's grievances
        return Grievance.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        grievance = serializer.save(
            user=self.request.user,
            department="Pending"
        )

        # Run AI detection async
        run_ai_detection.delay(grievance.id)

        # Send notification async
        create_notification.delay(
            grievance.user.id,
            f"Your grievance #{grievance.id} is submitted and under AI review."
        )
