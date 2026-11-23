


# from django.utils import timezone
# from django.core.mail import EmailMessage
# from django.conf import settings

# from rest_framework.viewsets import ModelViewSet
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.exceptions import PermissionDenied

# from apps.grievances.models import Grievance
# from apps.grievances.serializers import (
#     GrievanceSerializer,
#     GrievanceStatusUpdateSerializer,
# )

# from apps.notifications.tasks import create_notification
# from apps.grievances.tasks import send_grievance_email


# class OfficerGrievanceViewSet(ModelViewSet):
#     """
#     Officer:
#     - View grievances of own department
#     - Update grievance status
#     - Upload before/after proof images
#     """

#     permission_classes = [IsAuthenticated]

#     # -----------------------------------------------------
#     # 🔍 Officer can only see grievances of their department
#     # -----------------------------------------------------

#     def get_queryset(self):
#         user = self.request.user

#         if not user.is_staff or not user.department:
#             return Grievance.objects.none()

#         return Grievance.objects.filter(
#             department__iexact=user.department
#         ).order_by("-created_at")

#     # -----------------------------------------------------
#     # 📦 Serializer Selection
#     # -----------------------------------------------------

#     def get_serializer_class(self):
#         if self.action in ["partial_update", "update"]:
#             return GrievanceStatusUpdateSerializer

#         return GrievanceSerializer

#     # -----------------------------------------------------
#     # 🔄 Update grievance (status + proof images)
#     # -----------------------------------------------------

#     def perform_update(self, serializer):

#         grievance = self.get_object()

#         old_status = grievance.status
#         old_department = grievance.department

#         grievance = serializer.save()

#         # 👮 Assign officer automatically
#         if grievance.assigned_to is None:
#             grievance.assigned_to = self.request.user

#         # ✅ When resolved
#         if grievance.status.lower() == "resolved":
#             grievance.resolved_at = timezone.now()
#             grievance.resolved_by = self.request.user

#         grievance.save()

#         # -------------------------------------------------
#         # 🔔 In-app Notification
#         # -------------------------------------------------

#         create_notification.delay(
#             grievance.user.id,
#             f"Your grievance #{grievance.id} status changed to {grievance.status}"
#         )

#         # -------------------------------------------------
#         # 📧 EMAIL: Department Assigned
#         # -------------------------------------------------

#         if grievance.department != old_department:

#             send_grievance_email.delay(
#                 subject="Complaint Assigned to Department",
#                 message=f"""
# Hello {grievance.user.username},

# Your complaint '{grievance.title}' has been assigned to the {grievance.department} department.

# Our officer will review it soon.

# Smart Grievance System
# """,
#                 recipient_list=[grievance.user.email],
#             )

#         # -------------------------------------------------
#         # 📧 EMAIL: Status Updated
#         # -------------------------------------------------

#         if grievance.status != old_status:

#             send_grievance_email.delay(
#                 subject="Complaint Status Updated",
#                 message=f"""
# Hello {grievance.user.username},

# The status of your complaint '{grievance.title}' has been updated.

# New Status: {grievance.status}

# Smart Grievance System
# """,
#                 recipient_list=[grievance.user.email],
#             )

#         # -------------------------------------------------
#         # 📧 EMAIL: Complaint Resolved (WITH PROOF IMAGES)
#         # -------------------------------------------------

#         if grievance.status.lower() == "resolved":

#             subject = "Complaint Resolved with Proof"

#             message = f"""
# Hello {grievance.user.username},

# Your complaint '{grievance.title}' has been resolved successfully.

# Resolution Note:
# {grievance.resolution_note or "Work completed successfully."}

# Please see the attached proof images (Before and After).

# You can login to the Smart Grievance System to view details.

# Smart Grievance System
# """

#             email = EmailMessage(
#                 subject,
#                 message,
#                 settings.DEFAULT_FROM_EMAIL,
#                 [grievance.user.email],
#             )

#             # Attach Before Image
#             if grievance.before_image:
#                 email.attach_file(grievance.before_image.path)

#             # Attach After Image
#             if grievance.after_image:
#                 email.attach_file(grievance.after_image.path)

#             email.send()

#         # -------------------------------------------------
#         # 📧 EMAIL: Complaint Rejected
#         # -------------------------------------------------

#         if grievance.status.lower() == "rejected":

#             send_grievance_email.delay(
#                 subject="Complaint Rejected",
#                 message=f"""
# Hello {grievance.user.username},

# Your complaint '{grievance.title}' has been rejected after review.

# If you have further questions, please contact support.

# Smart Grievance System
# """,
#                 recipient_list=[grievance.user.email],
#             )

#     # -----------------------------------------------------
#     # ❌ Officers cannot delete grievances
#     # -----------------------------------------------------

#     def destroy(self, request, *args, **kwargs):
#         raise PermissionDenied("Officers cannot delete grievances")



# from django.utils import timezone
# from django.core.mail import EmailMessage
# from django.conf import settings

# from rest_framework.viewsets import ModelViewSet
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.exceptions import PermissionDenied

# from apps.grievances.models import Grievance, GrievanceDepartmentTask
# from apps.grievances.serializers import (
#     GrievanceSerializer,
#     GrievanceStatusUpdateSerializer,
# )

# from apps.notifications.tasks import create_notification
# from apps.grievances.tasks import send_grievance_email


# class OfficerGrievanceViewSet(ModelViewSet):

#     permission_classes = [IsAuthenticated]

#     # -----------------------------------------------------
#     # 🔍 Officer can only see grievances of their department
#     # -----------------------------------------------------
#     def get_queryset(self):
#         user = self.request.user

#         if not user.is_staff or not user.department:
#             return Grievance.objects.none()

#         return Grievance.objects.filter(
#             department__name__iexact=user.department
#         ).distinct().order_by("-created_at")

#     # -----------------------------------------------------
#     # 📦 Serializer Selection
#     # -----------------------------------------------------
#     def get_serializer_class(self):
#         if self.action in ["partial_update", "update"]:
#             return GrievanceStatusUpdateSerializer

#         return GrievanceSerializer

#     # -----------------------------------------------------
#     # 🔄 Officer updates ONLY their department task
#     # -----------------------------------------------------
#     def perform_update(self, serializer):

#         grievance = self.get_object()
#         officer = self.request.user

#         # 🔍 Find officer's department task
#         try:
#             task = GrievanceDepartmentTask.objects.get(
#                 grievance=grievance,
#                 department__name__iexact=officer.department
#             )
#         except GrievanceDepartmentTask.DoesNotExist:
#             raise PermissionDenied("You are not assigned to this grievance")

#         old_status = task.status
#         data = serializer.validated_data

#         # 📸 Update proof images (task-level)
#         if "before_image" in data:
#             task.before_image = data["before_image"]

#         if "after_image" in data:
#             task.after_image = data["after_image"]

#         if "resolution_note" in data:
#             task.resolution_note = data["resolution_note"]

#         # 🔄 Update task status
#         if "status" in data:
#             status = data["status"].lower()

#             if status == "resolved":
#                 task.status = "resolved"
#                 task.resolved_at = timezone.now()
#                 task.officer = officer

#             elif status == "in_progress":
#                 task.status = "in_progress"

#         task.save()

#         # 🔥 Update main grievance status correctly
#         grievance.update_status_from_departments()

#         # 🔔 Notification
#         create_notification.delay(
#             grievance.user.id,
#             f"{task.department.name} department updated your grievance #{grievance.id}"
#         )

#         # 📧 EMAIL: Department work completed
#         if task.status == "resolved" and old_status != "resolved":

#             subject = f"{task.department.name} Work Completed"

#             message = f"""
# Hello {grievance.user.username},

# The {task.department.name} department has completed their work for your complaint:

# "{grievance.title}"

# Resolution Note:
# {task.resolution_note or "Work completed successfully."}

# Other departments (if any) may still be working.

# Smart Grievance System
# """

#             email = EmailMessage(
#                 subject,
#                 message,
#                 settings.DEFAULT_FROM_EMAIL,
#                 [grievance.user.email],
#             )

#             if task.before_image:
#                 email.attach_file(task.before_image.path)

#             if task.after_image:
#                 email.attach_file(task.after_image.path)

#             email.send()

#         # 📧 EMAIL: Full complaint resolved
#         if grievance.status == "resolved":

#             send_grievance_email.delay(
#                 subject="Complaint Fully Resolved",
#                 message=f"""
# Hello {grievance.user.username},

# All departments have completed work for your complaint:

# "{grievance.title}"

# Your grievance is now fully RESOLVED.

# Thank you for using Smart Grievance System.
# """,
#                 recipient_list=[grievance.user.email],
#             )

#     # -----------------------------------------------------
#     # ❌ Officers cannot delete grievances
#     # -----------------------------------------------------
#     def destroy(self, request, *args, **kwargs):
#         raise PermissionDenied("Officers cannot delete grievances")


# from django.utils import timezone
# from django.core.mail import EmailMessage
# from django.conf import settings

# from rest_framework.viewsets import ModelViewSet
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.exceptions import PermissionDenied

# from apps.grievances.models import Grievance, GrievanceDepartmentTask
# from apps.grievances.serializers import (
#     GrievanceSerializer,
#     GrievanceStatusUpdateSerializer,
# )

# from apps.notifications.tasks import create_notification
# from apps.grievances.tasks import send_grievance_email


# class OfficerGrievanceViewSet(ModelViewSet):

#     permission_classes = [IsAuthenticated]

#     # -----------------------------------------------------
#     # 🔍 Officer can only see grievances of their department
#     # -----------------------------------------------------
#     def get_queryset(self):
#         user = self.request.user

#         if not user.is_staff or not user.department:
#             return Grievance.objects.none()

#         return Grievance.objects.filter(
#             department__name__iexact=user.department
#         ).distinct().order_by("-created_at")

#     # -----------------------------------------------------
#     # 📦 Serializer Selection
#     # -----------------------------------------------------
#     def get_serializer_class(self):
#         if self.action in ["partial_update", "update"]:
#             return GrievanceStatusUpdateSerializer

#         return GrievanceSerializer

#     # -----------------------------------------------------
#     # 🔄 Officer updates ONLY their department task
#     # -----------------------------------------------------
#     def perform_update(self, serializer):

#         grievance = self.get_object()
#         officer = self.request.user

#         # 🔍 Find officer's department task
#         try:
#             task = GrievanceDepartmentTask.objects.get(
#                 grievance=grievance,
#                 department__name__iexact=officer.department
#             )
#         except GrievanceDepartmentTask.DoesNotExist:
#             raise PermissionDenied("You are not assigned to this grievance")

#         old_status = task.status
#         data = serializer.validated_data

#         # 📸 Update proof images
#         if "before_image" in data:
#             task.before_image = data["before_image"]

#         if "after_image" in data:
#             task.after_image = data["after_image"]

#         if "resolution_note" in data:
#             task.resolution_note = data["resolution_note"]

#         # 🔄 Update task status
#         if "status" in data:
#             status = data["status"].lower()

#             if status == "resolved":
#                 task.status = "resolved"
#                 task.resolved_at = timezone.now()
#                 task.officer = officer

#             elif status == "in_progress":
#                 task.status = "in_progress"

#         task.save()

#         # 🔥 Update grievance status
#         grievance.update_status_from_departments()

#         # 🔔 Notification
#         create_notification.delay(
#             grievance.user.id,
#             f"{task.department.name} department updated your grievance #{grievance.id}"
#         )

#         # -------------------------------------------------
#         # 🔍 Build Pending Department Message
#         # -------------------------------------------------
#         pending_tasks = grievance.department_tasks.filter(
#             status__in=["pending", "in_progress"]
#         )

#         if pending_tasks.exists():
#             pending_names = ", ".join(
#                 [f"{t.department.name} dept" for t in pending_tasks]
#             )
#             pending_text = f"{pending_names} may still be working."
#         else:
#             pending_text = "All departments have completed their work."

#         # -------------------------------------------------
#         # 📧 EMAIL: Department work completed (UPDATED)
#         # -------------------------------------------------
#         if task.status == "resolved" and old_status != "resolved":

#             subject = f"{task.department.name} Work Completed"

#             message = f"""
# Hello {grievance.user.username},

# The {task.department.name} department has completed their work:

# "{grievance.title}"

# Resolution Note:
# {task.resolution_note or "Work completed successfully."}

# {pending_text}

# Attached:

# * Before Work Image
# * After Work Image

# Smart Grievance System
# """

#             email = EmailMessage(
#                 subject,
#                 message,
#                 settings.DEFAULT_FROM_EMAIL,
#                 [grievance.user.email],
#             )

#             # 📎 Attach images
#             if task.before_image:
#                 email.attach_file(task.before_image.path)

#             if task.after_image:
#                 email.attach_file(task.after_image.path)

#             email.send()

#         # -------------------------------------------------
#         # 📧 EMAIL: Full complaint resolved
#         # -------------------------------------------------
#         if grievance.status == "resolved":

#             send_grievance_email.delay(
#                 subject="Complaint Fully Resolved",
#                 message=f"""
# Hello {grievance.user.username},

# All departments have completed work for your complaint:

# "{grievance.title}"

# Your grievance is now fully RESOLVED.

# Thank you for using Smart Grievance System.
# """,
#                 recipient_list=[grievance.user.email],
#             )

#     # -----------------------------------------------------
#     # ❌ Officers cannot delete grievances
#     # -----------------------------------------------------
#     def destroy(self, request, *args, **kwargs):
#         raise PermissionDenied("Officers cannot delete grievances")



# from django.utils import timezone
# from django.core.mail import EmailMessage
# from django.conf import settings

# from rest_framework.viewsets import ModelViewSet
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.exceptions import PermissionDenied

# from rest_framework.response import Response  # 🔥 IMPORTANT

# from apps.grievances.models import Grievance, GrievanceDepartmentTask
# from apps.grievances.serializers import (
#     GrievanceSerializer,
#     GrievanceStatusUpdateSerializer,
# )

# from apps.notifications.tasks import create_notification
# from apps.grievances.tasks import send_grievance_email

# from apps.grievances.services.rejection_service import handle_rejection


# class OfficerGrievanceViewSet(ModelViewSet):

#     permission_classes = [IsAuthenticated]

#     # -----------------------------------------------------
#     # 🔍 Officer can only see grievances of their department
#     # -----------------------------------------------------
#     def get_queryset(self):
#         user = self.request.user

#         if not user.is_staff or not user.department:
#             return Grievance.objects.none()

#         return Grievance.objects.filter(
#             department__name__iexact=user.department
#         ).distinct().order_by("-created_at")

#     # -----------------------------------------------------
#     # 📦 Serializer Selection
#     # -----------------------------------------------------
#     def get_serializer_class(self):
#         if self.action in ["partial_update", "update"]:
#             return GrievanceStatusUpdateSerializer
#         return GrievanceSerializer

#     # -----------------------------------------------------
#     # 🔥 FINAL FIX: OVERRIDE UPDATE (VERY IMPORTANT)
#     # -----------------------------------------------------
#     def update(self, request, *args, **kwargs):

#         partial = kwargs.pop("partial", False)
#         instance = self.get_object()

#         # 🔥 ALWAYS USE PARENT FOR DUPLICATE
#         if instance.is_duplicate and instance.parent:
#             instance = instance.parent

#         serializer = self.get_serializer(
#             instance,
#             data=request.data,
#             partial=partial
#         )
#         serializer.is_valid(raise_exception=True)

#         officer = request.user
#         data = request.data

#         # =================================================
#         # 🚫 HANDLE REJECTION
#         # =================================================
#         status_value = serializer.validated_data.get("status")

#         if status_value == "rejected":

#             proof = request.FILES.get("rejection_proof")
#             reason = data.get("rejection_reason")

#             handle_rejection(
#                 grievance=instance,
#                 user=officer,
#                 proof=proof,
#                 reason=reason
#             )

#             create_notification.delay(
#                 instance.user.id,
#                 f"Your grievance #{instance.id} has been rejected."
#             )

#             # 🔥 RETURN UPDATED DATA (FIX)
#             return Response(
#                 GrievanceSerializer(instance, context={"request": request}).data
#             )

#         # =================================================
#         # 🔍 Find department task
#         # =================================================
#         try:
#             task = GrievanceDepartmentTask.objects.get(
#                 grievance=instance,
#                 department__name__iexact=officer.department
#             )
#         except GrievanceDepartmentTask.DoesNotExist:
#             raise PermissionDenied("You are not assigned to this grievance")

#         old_status = task.status
#         validated_data = serializer.validated_data

#         # 📸 Update images
#         if "before_image" in validated_data:
#             task.before_image = validated_data["before_image"]

#         if "after_image" in validated_data:
#             task.after_image = validated_data["after_image"]

#         if "resolution_note" in validated_data:
#             task.resolution_note = validated_data["resolution_note"]

#         # 🔄 Update status
#         if "status" in validated_data:
#             status = validated_data["status"].lower()

#             if status == "resolved":
#                 task.status = "resolved"
#                 task.resolved_at = timezone.now()
#                 task.officer = officer

#             elif status == "in_progress":
#                 task.status = "in_progress"

#         task.save()

#         # 🔥 Update grievance (this syncs duplicates)
#         instance.update_status_from_departments()

#         # 🔔 Notification
#         create_notification.delay(
#             instance.user.id,
#             f"{task.department.name} department updated your grievance #{instance.id}"
#         )

#         # -------------------------------------------------
#         # 📧 EMAIL LOGIC (unchanged)
#         # -------------------------------------------------
#         pending_tasks = instance.department_tasks.filter(
#             status__in=["pending", "in_progress"]
#         )

#         if pending_tasks.exists():
#             pending_text = ", ".join(
#                 [f"{t.department.name} dept" for t in pending_tasks]
#             )
#         else:
#             pending_text = "All departments completed."

#         if task.status == "resolved" and old_status != "resolved":

#             email = EmailMessage(
#                 f"{task.department.name} Work Completed",
#                 f"""
# Hello {instance.user.username},

# Work completed for:
# {instance.title}

# {pending_text}
# """,
#                 settings.DEFAULT_FROM_EMAIL,
#                 [instance.user.email],
#             )

#             if task.before_image:
#                 email.attach_file(task.before_image.path)

#             if task.after_image:
#                 email.attach_file(task.after_image.path)

#             email.send()

#         if instance.status == "resolved":

#             send_grievance_email.delay(
#                 subject="Complaint Fully Resolved",
#                 message=f"""
# Hello {instance.user.username},

# Your complaint is fully resolved.

# "{instance.title}"
# """,
#                 recipient_list=[instance.user.email],
#             )

#         # 🔥 FINAL RESPONSE FIX (MOST IMPORTANT)
#         return Response(
#             GrievanceSerializer(instance, context={"request": request}).data
#         )

#     # -----------------------------------------------------
#     # ❌ Delete blocked
#     # -----------------------------------------------------
#     def destroy(self, request, *args, **kwargs):
#         raise PermissionDenied("Officers cannot delete grievances")



from django.utils import timezone
from django.core.mail import EmailMessage
from django.conf import settings

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from apps.grievances.models import Grievance, GrievanceDepartmentTask
from apps.grievances.serializers import (
    GrievanceSerializer,
    GrievanceStatusUpdateSerializer,
)

from apps.notifications.tasks import create_notification
from apps.grievances.tasks import send_grievance_email
from apps.grievances.services.rejection_service import handle_rejection


class OfficerGrievanceViewSet(ModelViewSet):

    permission_classes = [IsAuthenticated]

    # -----------------------------------------------------
    # 🔍 Officer can only see grievances of their department
    # -----------------------------------------------------
    def get_queryset(self):
        user = self.request.user

        if not user.is_staff or not user.department:
            return Grievance.objects.none()

        return Grievance.objects.filter(
            department__name__iexact=user.department
        ).distinct().order_by("-created_at")

    # -----------------------------------------------------
    # 📦 Serializer Selection
    # -----------------------------------------------------
    def get_serializer_class(self):
        if self.action in ["partial_update", "update"]:
            return GrievanceStatusUpdateSerializer
        return GrievanceSerializer

    # -----------------------------------------------------
    # 🔥 FINAL FIXED UPDATE METHOD
    # -----------------------------------------------------
    def update(self, request, *args, **kwargs):

        partial = kwargs.pop("partial", False)
        instance = self.get_object()

        # 🔥 ALWAYS USE PARENT FOR DUPLICATE
        if instance.is_duplicate and instance.parent:
            instance = instance.parent

        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=partial
        )
        serializer.is_valid(raise_exception=True)

        officer = request.user
        data = request.data

        # =================================================
        # 🚫 HANDLE REJECTION
        # =================================================
        status_value = serializer.validated_data.get("status")

        if status_value == "rejected":

            proof = request.FILES.get("rejection_proof")
            reason = data.get("rejection_reason")

            handle_rejection(
                grievance=instance,
                user=officer,
                proof=proof,
                reason=reason
            )

            create_notification.delay(
                instance.user.id,
                f"Your grievance #{instance.id} has been rejected."
            )

            return Response(
                GrievanceSerializer(instance, context={"request": request}).data
            )

        # =================================================
        # 🔍 Find department task
        # =================================================
        try:
            task = GrievanceDepartmentTask.objects.get(
                grievance=instance,
                department__name__iexact=officer.department
            )
        except GrievanceDepartmentTask.DoesNotExist:
            raise PermissionDenied("You are not assigned to this grievance")

        old_status = task.status
        validated_data = serializer.validated_data

        # =================================================
        # 📸 UPDATE IMAGES (🔥 FIX)
        # =================================================
        if "before_image" in validated_data:
            task.before_image = validated_data["before_image"]
            instance.before_image = validated_data["before_image"]

        if "after_image" in validated_data:
            task.after_image = validated_data["after_image"]
            instance.after_image = validated_data["after_image"]   # 🔥 MAIN FIX

        if "resolution_note" in validated_data:
            task.resolution_note = validated_data["resolution_note"]
            instance.resolution_note = validated_data["resolution_note"]

        # =================================================
        # 🔄 UPDATE STATUS (🔥 FIXED)
        # =================================================
        if "status" in validated_data:
            status = validated_data["status"].lower()

            if status == "resolved":
                task.status = "resolved"
                task.resolved_at = timezone.now()
                task.officer = officer

                instance.status = "resolved"
                instance.resolved_at = timezone.now()
                instance.resolved_by = officer

            elif status == "in_progress":
                task.status = "in_progress"
                instance.status = "in_progress"

        task.save()
        instance.save()  # 🔥 IMPORTANT

        # 🔥 Sync overall grievance status
        instance.update_status_from_departments()

        # 🔔 Notification
        create_notification.delay(
            instance.user.id,
            f"{task.department.name} department updated your grievance #{instance.id}"
        )

        # -------------------------------------------------
        # 📧 EMAIL LOGIC
        # -------------------------------------------------
        pending_tasks = instance.department_tasks.filter(
            status__in=["pending", "in_progress"]
        )

        if pending_tasks.exists():
            pending_text = ", ".join(
                [f"{t.department.name} dept" for t in pending_tasks]
            )
        else:
            pending_text = "All departments completed."

        if task.status == "resolved" and old_status != "resolved":

            email = EmailMessage(
                f"{task.department.name} Work Completed",
                f"""
Hello {instance.user.username},

Work completed for:
{instance.title}

{pending_text}
""",
                settings.DEFAULT_FROM_EMAIL,
                [instance.user.email],
            )

            if task.before_image:
                email.attach_file(task.before_image.path)

            if task.after_image:
                email.attach_file(task.after_image.path)

            email.send()

        if instance.status == "resolved":

            send_grievance_email.delay(
                subject="Complaint Fully Resolved",
                message=f"""
Hello {instance.user.username},

Your complaint is fully resolved.

"{instance.title}"
""",
                recipient_list=[instance.user.email],
            )

        # =================================================
        # 🔥 FINAL RESPONSE
        # =================================================
        return Response(
            GrievanceSerializer(instance, context={"request": request}).data
        )

    # -----------------------------------------------------
    # ❌ Delete blocked
    # -----------------------------------------------------
    def destroy(self, request, *args, **kwargs):
        raise PermissionDenied("Officers cannot delete grievances")