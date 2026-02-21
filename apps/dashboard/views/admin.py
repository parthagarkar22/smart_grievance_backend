


#new changes



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser

from django.db.models import Count, Avg, F, ExpressionWrapper, DurationField, Q
from django.utils.timezone import now
from datetime import timedelta
from django.contrib.auth import get_user_model

from apps.grievances.models import Grievance
from apps.feedback.models import Feedback

User = get_user_model()


class AdminDashboardView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        grievances = Grievance.objects.all()
        last_30_days = now() - timedelta(days=30)

        # 🔹 Global Stats
        total = grievances.count()
        pending = grievances.filter(status="pending").count()
        in_progress = grievances.filter(status="in_progress").count()
        resolved = grievances.filter(status="resolved").count()

        # 🔹 Average Resolution Time
        resolved_cases = grievances.filter(
            status="resolved",
            resolved_at__isnull=False
        ).annotate(
            resolution_time=ExpressionWrapper(
                F("resolved_at") - F("created_at"),
                output_field=DurationField()
            )
        )

        avg_resolution_time = resolved_cases.aggregate(
            avg_time=Avg("resolution_time")
        )["avg_time"]

        # 🔹 Overall Average Rating
        avg_rating = Feedback.objects.aggregate(
            avg_rating=Avg("rating")
        )["avg_rating"]

        # 🔹 Department Performance
        department_stats = grievances.values("department").annotate(
            total=Count("id"),
            resolved=Count("id", filter=Q(status="resolved"))
        )

        # 🔹 Officer Performance
        officer_stats = []
        officers = User.objects.filter(is_staff=True)

        for officer in officers:
            officer_grievances = grievances.filter(assigned_to=officer)

            officer_stats.append({
                "officer_email": officer.email,
                "total_assigned": officer_grievances.count(),
                "resolved": officer_grievances.filter(status="resolved").count(),
                "pending": officer_grievances.filter(status="pending").count(),
                "average_rating": Feedback.objects.filter(
                    officer=officer
                ).aggregate(avg=Avg("rating"))["avg"]
            })

        return Response({
            "global_stats": {
                "total": total,
                "pending": pending,
                "in_progress": in_progress,
                "resolved": resolved,
                "average_resolution_time": avg_resolution_time,
                "average_rating": avg_rating
            },
            "department_stats": department_stats,
            "officer_stats": officer_stats,
            "last_30_days_count": grievances.filter(
                created_at__gte=last_30_days
            ).count(),
        })
