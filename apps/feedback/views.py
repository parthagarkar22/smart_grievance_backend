



# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated

# from apps.grievances.models import Grievance
# from .models import Feedback
# from .serializers import FeedbackSerializer


# class FeedbackCreateView(APIView):
#     permission_classes = [IsAuthenticated]

#     # ✅ GET API
#     def get(self, request):
#         grievance_id = request.query_params.get("grievance")

#         # If grievance id is provided → return feedback for that grievance
#         if grievance_id:
#             feedbacks = Feedback.objects.filter(
#                 grievance__id=grievance_id,
#                 grievance__user=request.user
#             )
#         else:
#             # Otherwise return all feedbacks of logged-in user
#             feedbacks = Feedback.objects.filter(
#                 grievance__user=request.user
#             )

#         serializer = FeedbackSerializer(feedbacks, many=True)
#         return Response(serializer.data)


#     # ✅ POST API (your existing logic)
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

#         if grievance.user != request.user:
#             return Response(
#                 {"error": "You are not authorized to give feedback for this grievance"},
#                 status=403
#             )

#         if grievance.status.lower() != "resolved":
#             return Response(
#                 {"error": "Feedback is allowed only after the grievance is resolved"},
#                 status=400
#             )

#         # Make sure your Grievance model has 'assigned_officer'
#         officer = grievance.assigned_officer

#         if not officer:
#             return Response(
#                 {"error": "No officer was assigned to this grievance. Cannot save feedback."},
#                 status=400
#             )

#         serializer = FeedbackSerializer(data=request.data)

#         if serializer.is_valid():
#             serializer.save(grievance=grievance, officer=officer)
#             return Response(serializer.data, status=201)

#         return Response(serializer.errors, status=400)


# class FeedbackAdminListView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         # Only admin/staff can view all feedback
#         if not request.user.is_staff:
#             return Response({"error": "Not authorized"}, status=403)

#         feedbacks = Feedback.objects.all().order_by('-created_at')
#         serializer = FeedbackSerializer(feedbacks, many=True)
#         return Response(serializer.data)


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

        # Check grievance owner
        if grievance.user != request.user:
            return Response(
                {"error": "You are not authorized to give feedback for this grievance"},
                status=403
            )

        # Allow feedback only if resolved
        if grievance.status.lower() != "resolved":
            return Response(
                {"error": "Feedback is allowed only after the grievance is resolved"},
                status=400
            )

        # ✅ Added correct field here
        officer = grievance.assigned_to

        if not officer:
            return Response(
                {"error": "No officer was assigned to this grievance. Cannot save feedback."},
                status=400
            )

        serializer = FeedbackSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(grievance=grievance, officer=officer)
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)


class FeedbackAdminListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not request.user.is_staff:
            return Response({"error": "Not authorized"}, status=403)

        feedbacks = Feedback.objects.all().order_by("-created_at")
        serializer = FeedbackSerializer(feedbacks, many=True)
        return Response(serializer.data)