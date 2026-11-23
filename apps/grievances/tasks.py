
# from celery import shared_task
# from django.utils import timezone
# from datetime import timedelta
# from django.core.mail import send_mail
# from django.conf import settings
# from django.contrib.auth import get_user_model

# from apps.grievances.models import Grievance
# from apps.departments.models import Department
# from apps.notifications.tasks import create_notification

# from common.utils import detect_department, detect_priority

# User = get_user_model()


# ======================================================
# 🔹 AI DETECTION TASK
# ======================================================

# @shared_task
# def run_ai_detection(grievance_id):

#     # Lazy import (prevents circular import)
#     from apps.grievances.ai.predictor import predict_image

#     grievance = Grievance.objects.get(id=grievance_id)

#     combined_text = f"{grievance.title} {grievance.description}"

#     # 🔹 TEXT detection
#     text_dept = detect_department(combined_text)
#     priority = detect_priority(combined_text)

#     image_dept = None
#     confidence = 0.0

#     # 🔹 IMAGE detection
#     if grievance.image:
#         image_dept, confidence = predict_image(grievance.image.path)

#     # ======================================================
#     # 🔥 USE SAME VARIABLE AS CELERY LOG
#     # ======================================================

#     if image_dept:
#         final_dept_name = image_dept.strip().capitalize()
#     else:
#         final_dept_name = text_dept.strip().capitalize()

#     # ======================================================
#     # 🔎 OPTIONAL: Match with Department table
#     # ======================================================

#     department_obj = Department.objects.filter(
#         name__iexact=final_dept_name
#     ).first()

#     if department_obj:
#         final_dept_name = department_obj.name

#     # ======================================================
#     # 🔥 FORCE UPDATE DATABASE
#     # ======================================================

#     Grievance.objects.filter(id=grievance_id).update(
#         department=final_dept_name,
#         detected_issue=image_dept,
#         ai_confidence=confidence,
#         priority=priority
#     )

#     # Reload updated object (for log verification)
#     grievance.refresh_from_db()

#     # ======================================================
#     # CELERY LOGS
#     # ======================================================

#     print("🧠 AI Prediction:", image_dept)
#     print("📊 Confidence:", confidence)
#     print("🏢 Department Saved:", grievance.department)

#     print(f"✅ AI Processing Completed for Grievance #{grievance.id}")



# from celery import shared_task
# from django.utils import timezone
# from datetime import timedelta
# from django.core.mail import send_mail
# from django.conf import settings
# from django.contrib.auth import get_user_model

# from apps.grievances.models import Grievance
# from apps.departments.models import Department
# from apps.notifications.tasks import create_notification

# from common.utils import detect_department, detect_priority

# User = get_user_model()
# @shared_task
# def run_ai_detection(grievance_id):

#     # Lazy import (prevents circular import)
#     from apps.grievances.ai.predictor import predict_image

#     grievance = Grievance.objects.get(id=grievance_id)

#     combined_text = f"{grievance.title} {grievance.description}"

#     # 🔹 TEXT detection
#     text_dept = detect_department(combined_text)
#     priority = detect_priority(combined_text)

#     image_depts = []
#     confidence = 0.0

#     # 🔹 IMAGE detection (MULTI LABEL)
#     if grievance.image:
#         image_depts, confidence = predict_image(grievance.image.path)

#     # ======================================================
#     # 🔥 FINAL DEPARTMENTS LOGIC
#     # ======================================================

#     if image_depts:
#         final_departments = [dept.strip().capitalize() for dept in image_depts]
#     else:
#         final_departments = [text_dept.strip().capitalize()]

#     # ======================================================
#     # 🔎 Match with Department table
#     # ======================================================

#     department_objs = Department.objects.filter(
#         name__in=final_departments
#     )

#     # ======================================================
#     # 🔥 UPDATE DATABASE
#     # ======================================================

#     grievance.priority = priority
#     grievance.ai_confidence = confidence
#     grievance.detected_issue = ", ".join(image_depts)

#     grievance.save()

#     # If using ManyToManyField for department
#     grievance.department.clear()

#     for dept in department_objs:
#         grievance.department.add(dept)

#     # Reload updated object
#     grievance.refresh_from_db()

#     # ======================================================
#     # CELERY LOGS
#     # ======================================================

#     print("🧠 AI Predictions:", image_depts)
#     print("📊 Confidence:", confidence)
#     print("🏢 Departments Saved:", [d.name for d in grievance.department.all()])

#     print(f"✅ AI Processing Completed for Grievance #{grievance.id}")

# # ======================================================
# # 🚨 ESCALATION TASK
# # ======================================================

# @shared_task
# def check_and_escalate_grievances():

#     now = timezone.now()

#     grievances = Grievance.objects.filter(
#         status__in=["pending", "in_progress"],
#         is_escalated=False
#     )

#     for grievance in grievances:

#         if grievance.priority == "CRITICAL":
#             escalation_days = 1
#         elif grievance.priority == "HIGH":
#             escalation_days = 2
#         elif grievance.priority == "MEDIUM":
#             escalation_days = 3
#         else:
#             escalation_days = 5

#         threshold_date = grievance.created_at + timedelta(days=escalation_days)

#         if now >= threshold_date:

#             grievance.status = "escalated"
#             grievance.is_escalated = True
#             grievance.escalated_at = now
#             grievance.save()

#             admins = User.objects.filter(is_superuser=True)

#             for admin in admins:
#                 create_notification.delay(
#                     admin.id,
#                     f"🚨 Grievance #{grievance.id} has been escalated."
#                 )

#             print(f"🚨 Grievance #{grievance.id} escalated.")


# # ======================================================
# # 📧 EMAIL TASK
# # ======================================================

# @shared_task
# def send_grievance_email(subject, message, recipient_list):

#     send_mail(
#         subject=subject,
#         message=message,
#         from_email=settings.DEFAULT_FROM_EMAIL,
#         recipient_list=recipient_list,
#         fail_silently=False,
#     )



# from celery import shared_task
# from django.utils import timezone
# from datetime import timedelta
# from django.core.mail import send_mail
# from django.conf import settings
# from django.contrib.auth import get_user_model

# from apps.grievances.models import Grievance
# from apps.departments.models import Department
# from apps.notifications.tasks import create_notification

# from common.utils import (
#     detect_department,
#     detect_priority,
#     final_department_decision
# )

# User = get_user_model()

# # ======================================================
# # 🤖 AI DETECTION TASK
# # ======================================================

# @shared_task
# def run_ai_detection(grievance_id):

#     # Lazy import (prevents circular import)
#     from apps.grievances.ai.predictor import predict_image

#     grievance = Grievance.objects.get(id=grievance_id)

#     combined_text = f"{grievance.title} {grievance.description}"

#     # ------------------------------------------------------
#     # TEXT DETECTION
#     # ------------------------------------------------------

#     text_depts = detect_department(combined_text)
#     priority = detect_priority(combined_text)

#     # ------------------------------------------------------
#     # IMAGE DETECTION
#     # ------------------------------------------------------

#     image_depts = []
#     confidence = 0.0

#     if grievance.image:
#         image_depts, confidence = predict_image(grievance.image.path)

#     # ------------------------------------------------------
#     # FINAL DEPARTMENT DECISION (IMAGE + TEXT)
#     # ------------------------------------------------------

#     final_departments = final_department_decision(
#         text_depts,
#         image_depts
#     )

#     # Normalize names
#     final_departments = [d.strip().capitalize() for d in final_departments]

#     # ------------------------------------------------------
#     # MATCH WITH DATABASE DEPARTMENTS
#     # ------------------------------------------------------

#     department_objs = Department.objects.filter(
#         name__in=final_departments
#     )

#     # ------------------------------------------------------
#     # UPDATE GRIEVANCE
#     # ------------------------------------------------------

#     grievance.priority = priority
#     grievance.ai_confidence = confidence
#     grievance.detected_issue = ", ".join(image_depts)

#     grievance.save()

#     # Clear existing departments
#     grievance.department.clear()

#     # Add multiple departments
#     for dept in department_objs:
#         grievance.department.add(dept)

#     grievance.refresh_from_db()

#     # ------------------------------------------------------
#     # DEBUG LOGS
#     # ------------------------------------------------------

#     print("🧠 TEXT Departments:", text_depts)
#     print("🧠 IMAGE Departments:", image_depts)
#     print("🏁 FINAL Departments:", final_departments)
#     print("📊 Confidence:", confidence)
#     print("🏢 Departments Saved:", [d.name for d in grievance.department.all()])

#     print(f"✅ AI Processing Completed for Grievance #{grievance.id}")


# # ======================================================
# # 🚨 ESCALATION TASK
# # ======================================================

# @shared_task
# def check_and_escalate_grievances():

#     now = timezone.now()

#     grievances = Grievance.objects.filter(
#         status__in=["pending", "in_progress"],
#         is_escalated=False
#     )

#     for grievance in grievances:

#         if grievance.priority == "CRITICAL":
#             escalation_days = 1
#         elif grievance.priority == "HIGH":
#             escalation_days = 2
#         elif grievance.priority == "MEDIUM":
#             escalation_days = 3
#         else:
#             escalation_days = 5

#         threshold_date = grievance.created_at + timedelta(days=escalation_days)

#         if now >= threshold_date:

#             grievance.status = "escalated"
#             grievance.is_escalated = True
#             grievance.escalated_at = now
#             grievance.save()

#             admins = User.objects.filter(is_superuser=True)

#             for admin in admins:
#                 create_notification.delay(
#                     admin.id,
#                     f"🚨 Grievance #{grievance.id} has been escalated."
#                 )

#             print(f"🚨 Grievance #{grievance.id} escalated.")


# # ======================================================
# # 📧 EMAIL TASK
# # ======================================================

# @shared_task
# def send_grievance_email(subject, message, recipient_list):

#     send_mail(
#         subject=subject,
#         message=message,
#         from_email=settings.DEFAULT_FROM_EMAIL,
#         recipient_list=recipient_list,
#         fail_silently=False,
#     )



# from celery import shared_task
# from django.utils import timezone
# from datetime import timedelta
# from django.core.mail import send_mail
# from django.conf import settings
# from django.contrib.auth import get_user_model

# from apps.grievances.models import Grievance, GrievanceDepartmentTask
# from apps.departments.models import Department
# from apps.notifications.tasks import create_notification

# from common.utils import (
#     detect_department,
#     detect_priority,
#     final_department_decision
# )

# User = get_user_model()

# # ======================================================
# # 🤖 AI DETECTION TASK
# # ======================================================

# @shared_task
# def run_ai_detection(grievance_id):

#     # Lazy import (prevents circular import)
#     from apps.grievances.ai.predictor import predict_image

#     grievance = Grievance.objects.get(id=grievance_id)

#     combined_text = f"{grievance.title} {grievance.description}"

#     # ------------------------------------------------------
#     # TEXT DETECTION
#     # ------------------------------------------------------

#     text_depts = detect_department(combined_text)
#     priority = detect_priority(combined_text)

#     # ------------------------------------------------------
#     # IMAGE DETECTION
#     # ------------------------------------------------------

#     image_depts = []
#     confidence = 0.0

#     if grievance.image:
#         image_depts, confidence = predict_image(grievance.image.path)

#     # ------------------------------------------------------
#     # FINAL DEPARTMENT DECISION
#     # ------------------------------------------------------

#     final_departments = final_department_decision(
#         text_depts,
#         image_depts
#     )

#     final_departments = [d.strip().capitalize() for d in final_departments]

#     # ------------------------------------------------------
#     # MATCH WITH DATABASE DEPARTMENTS
#     # ------------------------------------------------------

#     department_objs = Department.objects.filter(
#         name__in=final_departments
#     )

#     # ------------------------------------------------------
#     # UPDATE GRIEVANCE BASIC INFO
#     # ------------------------------------------------------

#     grievance.priority = priority
#     grievance.ai_confidence = confidence
#     grievance.detected_issue = ", ".join(image_depts)

#     grievance.save()

#     # ------------------------------------------------------
#     # UPDATE MANY-TO-MANY DEPARTMENT FIELD
#     # (for filtering & dashboards)
#     # ------------------------------------------------------

#     grievance.department.clear()

#     for dept in department_objs:
#         grievance.department.add(dept)

#     # ------------------------------------------------------
#     # CREATE DEPARTMENT TASKS
#     # ------------------------------------------------------

#     # remove old tasks if AI re-runs
#     GrievanceDepartmentTask.objects.filter(
#         grievance=grievance
#     ).delete()

#     for dept in department_objs:
#         GrievanceDepartmentTask.objects.create(
#             grievance=grievance,
#             department=dept,
#             status="pending"
#         )

#     grievance.refresh_from_db()

#     # ------------------------------------------------------
#     # DEBUG LOGS
#     # ------------------------------------------------------

#     print("🧠 TEXT Departments:", text_depts)
#     print("🧠 IMAGE Departments:", image_depts)
#     print("🏁 FINAL Departments:", final_departments)
#     print("📊 Confidence:", confidence)

#     print(
#         "🏢 Department Tasks Created:",
#         list(
#             grievance.department_tasks.values_list(
#                 "department__name",
#                 flat=True
#             )
#         )
#     )

#     print(f"✅ AI Processing Completed for Grievance #{grievance.id}")


# # ======================================================
# # 🚨 ESCALATION TASK
# # ======================================================

# @shared_task
# def check_and_escalate_grievances():

#     now = timezone.now()

#     grievances = Grievance.objects.filter(
#         status__in=["pending", "in_progress"],
#         is_escalated=False
#     )

#     for grievance in grievances:

#         if grievance.priority == "CRITICAL":
#             escalation_days = 1
#         elif grievance.priority == "HIGH":
#             escalation_days = 2
#         elif grievance.priority == "MEDIUM":
#             escalation_days = 3
#         else:
#             escalation_days = 5

#         threshold_date = grievance.created_at + timedelta(days=escalation_days)

#         if now >= threshold_date:

#             grievance.status = "escalated"
#             grievance.is_escalated = True
#             grievance.escalated_at = now
#             grievance.save()

#             admins = User.objects.filter(is_superuser=True)

#             for admin in admins:
#                 create_notification.delay(
#                     admin.id,
#                     f"🚨 Grievance #{grievance.id} has been escalated."
#                 )

#             print(f"🚨 Grievance #{grievance.id} escalated.")


# # ======================================================
# # 📧 EMAIL TASK
# # ======================================================

# @shared_task
# def send_grievance_email(subject, message, recipient_list):

#     send_mail(
#         subject=subject,
#         message=message,
#         from_email=settings.DEFAULT_FROM_EMAIL,
#         recipient_list=recipient_list,
#         fail_silently=False,
#     )

    


from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model

from apps.grievances.models import Grievance, GrievanceDepartmentTask
from apps.departments.models import Department
from apps.notifications.tasks import create_notification

from common.utils import (
    detect_department,
    detect_priority,
    final_department_decision
)

User = get_user_model()


# ======================================================
# 🤖 AI DETECTION TASK
# ======================================================

@shared_task
def run_ai_detection(grievance_id):

    # Lazy import (prevents circular import)
    from apps.grievances.ai.predictor import predict_image

    grievance = Grievance.objects.get(id=grievance_id)

    # ------------------------------------------------------
    # 🔥 SKIP AI FOR DUPLICATES (IMPORTANT OPTIMIZATION)
    # ------------------------------------------------------
    if grievance.is_duplicate and grievance.parent:
        parent = grievance.parent

        # Copy AI results from parent
        grievance.priority = parent.priority
        grievance.ai_confidence = parent.ai_confidence
        grievance.detected_issue = parent.detected_issue

        grievance.department.set(parent.department.all())
        grievance.save()

        print(f"⚡ Skipped AI (duplicate of #{parent.id})")
        return

    combined_text = f"{grievance.title} {grievance.description}"

    # ------------------------------------------------------
    # TEXT DETECTION
    # ------------------------------------------------------

    text_depts = detect_department(combined_text)
    priority = detect_priority(combined_text)

    # ------------------------------------------------------
    # IMAGE DETECTION
    # ------------------------------------------------------

    image_depts = []
    confidence = 0.0

    if grievance.image:
        image_depts, confidence = predict_image(grievance.image.path)

    # ------------------------------------------------------
    # FINAL DEPARTMENT DECISION
    # ------------------------------------------------------

    final_departments = final_department_decision(
        text_depts,
        image_depts
    )

    final_departments = [d.strip().capitalize() for d in final_departments]

    # ------------------------------------------------------
    # MATCH WITH DATABASE DEPARTMENTS
    # ------------------------------------------------------

    department_objs = Department.objects.filter(
        name__in=final_departments
    )

    # ------------------------------------------------------
    # UPDATE GRIEVANCE BASIC INFO
    # ------------------------------------------------------

    grievance.priority = priority
    grievance.ai_confidence = confidence
    grievance.detected_issue = ", ".join(image_depts)

    grievance.save()

    # ------------------------------------------------------
    # UPDATE MANY-TO-MANY DEPARTMENT FIELD
    # ------------------------------------------------------

    grievance.department.clear()

    for dept in department_objs:
        grievance.department.add(dept)

    # ------------------------------------------------------
    # CREATE DEPARTMENT TASKS
    # ------------------------------------------------------

    # Remove old tasks if AI re-runs
    GrievanceDepartmentTask.objects.filter(
        grievance=grievance
    ).delete()

    for dept in department_objs:
        GrievanceDepartmentTask.objects.create(
            grievance=grievance,
            department=dept,
            status="pending"
        )

    grievance.refresh_from_db()

    # ------------------------------------------------------
    # DEBUG LOGS
    # ------------------------------------------------------

    print("🧠 TEXT Departments:", text_depts)
    print("🧠 IMAGE Departments:", image_depts)
    print("🏁 FINAL Departments:", final_departments)
    print("📊 Confidence:", confidence)

    print(
        "🏢 Department Tasks Created:",
        list(
            grievance.department_tasks.values_list(
                "department__name",
                flat=True
            )
        )
    )

    print(f"✅ AI Processing Completed for Grievance #{grievance.id}")


# ======================================================
# 🚨 ESCALATION TASK
# ======================================================

@shared_task
def check_and_escalate_grievances():

    now = timezone.now()

    grievances = Grievance.objects.filter(
        status__in=["pending", "in_progress"],
        is_escalated=False
    )

    for grievance in grievances:

        if grievance.priority == "CRITICAL":
            escalation_days = 1
        elif grievance.priority == "HIGH":
            escalation_days = 2
        elif grievance.priority == "MEDIUM":
            escalation_days = 3
        else:
            escalation_days = 5

        threshold_date = grievance.created_at + timedelta(days=escalation_days)

        if now >= threshold_date:

            grievance.status = "escalated"
            grievance.is_escalated = True
            grievance.escalated_at = now
            grievance.save()

            admins = User.objects.filter(is_superuser=True)

            for admin in admins:
                create_notification.delay(
                    admin.id,
                    f"🚨 Grievance #{grievance.id} has been escalated."
                )

            print(f"🚨 Grievance #{grievance.id} escalated.")


# ======================================================
# 📧 EMAIL TASK
# ======================================================

@shared_task
def send_grievance_email(subject, message, recipient_list):

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=recipient_list,
        fail_silently=False,
    )