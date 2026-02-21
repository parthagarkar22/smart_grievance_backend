from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils.timezone import now
from datetime import timedelta
from django.db.models import Count

from apps.grievances.models import Grievance


class CitizenDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        grievances = Grievance.objects.filter(user=request.user)

        last_30_days = now() - timedelta(days=30)

        return Response({
            "total": grievances.count(),
            "pending": grievances.filter(status="pending").count(),
            "in_progress": grievances.filter(status="in_progress").count(),
            "resolved": grievances.filter(status="resolved").count(),
            "last_30_days_count": grievances.filter(
                created_at__gte=last_30_days
            ).count(),
        })
