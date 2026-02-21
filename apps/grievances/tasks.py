
# from celery import shared_task
# from apps.grievances.models import Grievance
# from apps.departments.models import Department
# from common.utils import detect_department, detect_priority


# @shared_task
# def run_ai_detection(grievance_id):

#     # 🔥 Lazy import (prevents circular import)
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

#     # 🔥 Hybrid decision logic
#     if image_dept and confidence > 0.75:
#         final_dept_name = image_dept.strip().capitalize()
#     else:
#         final_dept_name = text_dept.strip().capitalize()

#     print("FINAL_DEPT_NAME:", final_dept_name)

#     # 🔹 Match with Department table
#     department_obj = Department.objects.filter(
#         name__iexact=final_dept_name
#     ).first()

#     print("DEPARTMENT FOUND:", department_obj)

#     # ✅ Replace "Pending" with real department
#     if department_obj:
#         grievance.department = department_obj.name
#     else:
#         grievance.department = "General"

#     # ✅ Store AI metadata
#     grievance.detected_issue = image_dept
#     grievance.ai_confidence = confidence

#     grievance.priority = priority
#     grievance.save()

#     print(f"✅ AI Processing Completed for Grievance #{grievance.id}")







from celery import shared_task
from django.utils import timezone
from datetime import timedelta

from apps.grievances.models import Grievance
from apps.departments.models import Department
from apps.notifications.tasks import create_notification
from django.contrib.auth import get_user_model

from common.utils import detect_department, detect_priority

User = get_user_model()


# ======================================================
# 🔹 AI DETECTION TASK
# ======================================================

@shared_task
def run_ai_detection(grievance_id):

    # 🔥 Lazy import (prevents circular import)
    from apps.grievances.ai.predictor import predict_image

    grievance = Grievance.objects.get(id=grievance_id)

    combined_text = f"{grievance.title} {grievance.description}"

    # 🔹 TEXT detection
    text_dept = detect_department(combined_text)
    priority = detect_priority(combined_text)

    image_dept = None
    confidence = 0.0

    # 🔹 IMAGE detection
    if grievance.image:
        image_dept, confidence = predict_image(grievance.image.path)

    # 🔥 Hybrid decision logic
    if image_dept and confidence > 0.5:
        final_dept_name = str(image_dept).strip().capitalize()
    else:
        final_dept_name = text_dept.strip().capitalize()

    # 🔹 Match with Department table
    department_obj = Department.objects.filter(
        name__iexact=final_dept_name
    ).first()

    # ✅ Replace "Pending" with real department
    if department_obj:
        grievance.department = department_obj.name
    else:
        grievance.department = "General"

    # ✅ Store AI metadata
    grievance.detected_issue = image_dept
    grievance.ai_confidence = confidence
    grievance.priority = priority

    grievance.save()

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

        # 🔥 Priority-based escalation days
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

            # 🔔 Notify all superusers (higher authority)
            admins = User.objects.filter(is_superuser=True)

            for admin in admins:
                create_notification.delay(
                    admin.id,
                    f"🚨 Grievance #{grievance.id} has been escalated."
                )

            print(f"🚨 Grievance #{grievance.id} escalated.")
