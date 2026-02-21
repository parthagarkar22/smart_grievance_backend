
#changes



from django.db.models import Avg, F, ExpressionWrapper, DurationField
from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.grievances.models import Grievance
from apps.feedback.models import Feedback


class OfficerDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        officer = request.user

        # 🔹 Only grievances assigned to this officer
        grievances = Grievance.objects.filter(assigned_to=officer)

        total_cases = grievances.count()
        pending_cases = grievances.filter(status="pending").count()
        in_progress_cases = grievances.filter(status="in_progress").count()
        resolved_cases = grievances.filter(status="resolved").count()

        # 🔹 Average Resolution Time
        resolved_queryset = grievances.filter(
            status="resolved",
            resolved_at__isnull=False
        ).annotate(
            resolution_time=ExpressionWrapper(
                F("resolved_at") - F("created_at"),
                output_field=DurationField()
            )
        )

        avg_resolution_time = resolved_queryset.aggregate(
            avg_time=Avg("resolution_time")
        )["avg_time"]

        # 🔹 Average Rating
        avg_rating = Feedback.objects.filter(
            officer=officer
        ).aggregate(
            avg_rating=Avg("rating")
        )["avg_rating"]

        return Response({
            "total_assigned": total_cases,
            "pending": pending_cases,
            "in_progress": in_progress_cases,
            "resolved": resolved_cases,
            "average_resolution_time": avg_resolution_time,
            "average_rating": avg_rating,
        })
