from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.grievances.models import Grievance
from .models import Feedback
from .serializers import FeedbackSerializer


class FeedbackCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        grievance_id = request.data.get("grievance")

        try:
            grievance = Grievance.objects.get(id=grievance_id)
        except Grievance.DoesNotExist:
            return Response({"error": "Grievance not found"}, status=404)

        if grievance.status != "resolved":
            return Response(
                {"error": "Feedback allowed only after resolution"},
                status=400
            )

        if grievance.user != request.user:
            return Response({"error": "Not allowed"}, status=403)

        serializer = FeedbackSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(grievance=grievance)
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)
