


# from rest_framework.viewsets import ModelViewSet
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.parsers import MultiPartParser, FormParser

# from apps.grievances.models import Grievance
# from apps.grievances.serializers import GrievanceSerializer
# from apps.grievances.tasks import run_ai_detection, send_grievance_email
# from apps.notifications.tasks import create_notification


# class GrievanceViewSet(ModelViewSet):
#     serializer_class = GrievanceSerializer
#     queryset = Grievance.objects.all()
#     permission_classes = [IsAuthenticated]
#     parser_classes = (MultiPartParser, FormParser)

#     def get_queryset(self):
#         # Show only logged-in user's grievances
#         return Grievance.objects.filter(user=self.request.user)

#     def perform_create(self, serializer):
#         grievance = serializer.save(
#             user=self.request.user,
#             department="Pending"
#         )

#         # 🚀 Run AI detection async
#         run_ai_detection.delay(grievance.id)

#         # 🔔 Send in-app notification
#         create_notification.delay(
#             grievance.user.id,
#             f"Your grievance #{grievance.id} is submitted and under AI review."
#         )

#         # 📧 Send Email Notification
#         send_grievance_email.delay(
#             subject="Complaint Submitted Successfully",
#             message=f"""
# Hello {grievance.user.username},

# Your complaint '{grievance.title}' has been submitted successfully.

# Complaint ID: {grievance.id}
# Current Status: Pending

# Our team will review your complaint soon.

# Thank you,
# Smart Grievance Team
# """,
#             recipient_list=[grievance.user.email],
#         )



# from rest_framework.viewsets import ModelViewSet
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.parsers import MultiPartParser, FormParser

# from apps.grievances.models import Grievance
# from apps.grievances.serializers import GrievanceSerializer
# from apps.grievances.tasks import run_ai_detection, send_grievance_email
# from apps.notifications.tasks import create_notification


# class GrievanceViewSet(ModelViewSet):
#     serializer_class = GrievanceSerializer
#     queryset = Grievance.objects.all()
#     permission_classes = [IsAuthenticated]
#     parser_classes = (MultiPartParser, FormParser)

#     def get_queryset(self):
#         # Show only logged-in user's grievances
#         return Grievance.objects.filter(user=self.request.user)

#     def perform_create(self, serializer):

#         # Create grievance WITHOUT department
#         grievance = serializer.save(
#             user=self.request.user
#         )

#         # 🚀 Run AI detection async
#         run_ai_detection.delay(grievance.id)

#         # 🔔 Send in-app notification
#         create_notification.delay(
#             grievance.user.id,
#             f"Your grievance #{grievance.id} is submitted and under AI review."
#         )

#         # 📧 Send Email Notification
#         send_grievance_email.delay(
#             subject="Complaint Submitted Successfully",
#             message=f"""
# Hello {grievance.user.username},

# Your complaint '{grievance.title}' has been submitted successfully.

# Complaint ID: {grievance.id}
# Current Status: Pending

# Our AI system is analyzing the complaint and will assign it to the appropriate department(s).

# Thank you,
# Smart Grievance Team
# """,
#             recipient_list=[grievance.user.email],
#         )



# from rest_framework.viewsets import ModelViewSet
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.parsers import MultiPartParser, FormParser
# from rest_framework.exceptions import ValidationError  # ✅ NEW

# from apps.grievances.models import Grievance
# from apps.grievances.serializers import GrievanceSerializer
# from apps.grievances.tasks import run_ai_detection, send_grievance_email
# from apps.notifications.tasks import create_notification


# class GrievanceViewSet(ModelViewSet):
#     serializer_class = GrievanceSerializer
#     queryset = Grievance.objects.all()
#     permission_classes = [IsAuthenticated]
#     parser_classes = (MultiPartParser, FormParser)

#     # -----------------------------------------------------
#     # 👤 Show only logged-in user's grievances
#     # -----------------------------------------------------
#     def get_queryset(self):
#         return Grievance.objects.filter(user=self.request.user)

#     # -----------------------------------------------------
#     # 🚫 BLOCKED USER CHECK + CREATE
#     # -----------------------------------------------------
#     def perform_create(self, serializer):

#         user = self.request.user

#         # 🚫 Prevent blocked users
#         if user.is_blocked:
#             raise ValidationError({
#                 "error": "Your account is blocked due to multiple fake complaints."
#             })

#         # ✅ Create grievance
#         grievance = serializer.save(user=user)

#         # 🚀 Run AI detection async
#         run_ai_detection.delay(grievance.id)

#         # 🔔 Send in-app notification
#         create_notification.delay(
#             grievance.user.id,
#             f"Your grievance #{grievance.id} is submitted and under AI review."
#         )

#         # 📧 Send Email Notification
#         send_grievance_email.delay(
#             subject="Complaint Submitted Successfully",
#             message=f"""
# Hello {grievance.user.username},

# Your complaint '{grievance.title}' has been submitted successfully.

# Complaint ID: {grievance.id}
# Current Status: Pending

# Our AI system is analyzing the complaint and will assign it to the appropriate department(s).

# Thank you,
# Smart Grievance Team
# """,
#             recipient_list=[grievance.user.email],
#         )


from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.exceptions import ValidationError

from django.contrib.gis.geos import Point

from apps.grievances.models import Grievance
from apps.grievances.serializers import GrievanceSerializer
from apps.grievances.tasks import run_ai_detection, send_grievance_email
from apps.notifications.tasks import create_notification

# 🔥 AI + Duplicate
from apps.grievances.utils import (
    get_text_embedding,
    get_image_embedding,
)
from apps.grievances.services.duplicate_detection import find_duplicate


class GrievanceViewSet(ModelViewSet):
    serializer_class = GrievanceSerializer
    queryset = Grievance.objects.all()
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    # -----------------------------------------------------
    # 👤 Show only logged-in user's grievances
    # -----------------------------------------------------
    def get_queryset(self):
        return Grievance.objects.filter(user=self.request.user)

    # -----------------------------------------------------
    # 🚫 CREATE GRIEVANCE (FINAL CLEAN VERSION 🔥)
    # -----------------------------------------------------
    def perform_create(self, serializer):

        user = self.request.user

        # 🚫 Prevent blocked users
        if user.is_blocked:
            raise ValidationError({
                "error": "Your account is blocked due to multiple fake complaints."
            })

        # -----------------------------------------------------
        # 📍 LOCATION
        # -----------------------------------------------------
        latitude = self.request.data.get("latitude")
        longitude = self.request.data.get("longitude")

        if not latitude or not longitude:
            raise ValidationError({"error": "Latitude and Longitude are required."})

        try:
            location = Point(float(longitude), float(latitude))
        except Exception:
            raise ValidationError({"error": "Invalid latitude/longitude format."})

        # -----------------------------------------------------
        # 📸 IMAGE
        # -----------------------------------------------------
        image = self.request.FILES.get("image")

        # -----------------------------------------------------
        # 🧠 CREATE OBJECT
        # -----------------------------------------------------
        grievance = serializer.save(
            user=user,
            location=location
        )

        # ✅ ADD FIRST USER (IMPORTANT)
        grievance.linked_users.add(user)

        # -----------------------------------------------------
        # 🧠 EMBEDDINGS
        # -----------------------------------------------------
        grievance.text_embedding = get_text_embedding(grievance.title)

        if image:
            grievance.image = image
            grievance.save()
            grievance.image_embedding = get_image_embedding(grievance.image.path)

        grievance.save()

        # -----------------------------------------------------
        # 🔍 DUPLICATE DETECTION
        # -----------------------------------------------------
        duplicate = find_duplicate(grievance)

        if duplicate:
            grievance.is_duplicate = True
            grievance.parent = duplicate
            grievance.save()

            # 🔥 Add user to parent complaint
            duplicate.linked_users.add(user)

            # 🔥 RUN AI TASK FOR DUPLICATE ALSO (IMPORTANT FIX)
            run_ai_detection.delay(grievance.id)

            # 🔔 Notify user
            create_notification.delay(
                user.id,
                f"This issue already reported by {duplicate.linked_users.count()} users. Linked to complaint #{duplicate.id}"
            )

            return

        # -----------------------------------------------------
        # 🆕 NEW COMPLAINT FLOW
        # -----------------------------------------------------

        # 🚀 Run AI detection
        run_ai_detection.delay(grievance.id)

        # 🔔 Notification
        create_notification.delay(
            grievance.user.id,
            f"Your grievance #{grievance.id} is submitted and under AI review."
        )

        # 📧 Email
        send_grievance_email.delay(
            subject="Complaint Submitted Successfully",
            message=f"""
Hello {grievance.user.username},

Your complaint '{grievance.title}' has been submitted successfully.

Complaint ID: {grievance.id}
Current Status: Pending

Our AI system is analyzing the complaint and will assign it to the appropriate department(s).

Thank you,
Smart Grievance Team
""",
            recipient_list=[grievance.user.email],
        )