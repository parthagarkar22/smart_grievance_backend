# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated

# from apps.grievances.models import Grievance
# from .models import Feedback
# from .serializers import FeedbackSerializer


# class FeedbackCreateView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         grievance_id = request.data.get("grievance")

#         try:
#             grievance = Grievance.objects.get(id=grievance_id)
#         except Grievance.DoesNotExist:
#             return Response({"error": "Grievance not found"}, status=404)

#         if grievance.status != "resolved":
#             return Response(
#                 {"error": "Feedback allowed only after resolution"},
#                 status=400
#             )

#         if grievance.user != request.user:
#             return Response({"error": "Not allowed"}, status=403)

#         serializer = FeedbackSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(grievance=grievance)
#             return Response(serializer.data, status=201)

#         return Response(serializer.errors, status=400)




from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.grievances.models import Grievance
from .models import Feedback
from .serializers import FeedbackSerializer


class FeedbackCreateView(APIView):
    permission_classes = [IsAuthenticated]

    # ✅ GET API
    def get(self, request):
        grievance_id = request.query_params.get("grievance")

        # If grievance id is provided → return feedback for that grievance
        if grievance_id:
            feedbacks = Feedback.objects.filter(
                grievance__id=grievance_id,
                grievance__user=request.user
            )
        else:
            # Otherwise return all feedbacks of logged-in user
            feedbacks = Feedback.objects.filter(
                grievance__user=request.user
            )

        serializer = FeedbackSerializer(feedbacks, many=True)
        return Response(serializer.data)


    # ✅ POST API (your existing logic)
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
