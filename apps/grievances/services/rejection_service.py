


from rest_framework.exceptions import ValidationError
from apps.grievances.models import Grievance
from common.constants import MAX_REJECTION_LIMIT


def handle_rejection(grievance, user, proof, reason):

    # --------------------------------------------------
    # ✅ VALIDATION
    # --------------------------------------------------
    if not proof:
        raise ValidationError("Rejection proof image is required")

    if not reason:
        raise ValidationError("Rejection reason is required")

    # --------------------------------------------------
    # 🔥 ALWAYS USE PARENT (IMPORTANT)
    # --------------------------------------------------
    if grievance.is_duplicate and grievance.parent:
        grievance = grievance.parent

    # --------------------------------------------------
    # 🔥 UPDATE MAIN (PARENT)
    # --------------------------------------------------
    grievance.status = "rejected"
    grievance.rejection_proof = proof
    grievance.rejection_reason = reason
    grievance.rejected_by = user
    grievance.save()

    # --------------------------------------------------
    # 🔥🔥🔥 CRITICAL FIX: UPDATE ALL DUPLICATES
    # --------------------------------------------------
    duplicates = grievance.duplicates.all()

    for dup in duplicates:
        dup.status = "rejected"
        dup.rejection_proof = proof
        dup.rejection_reason = reason
        dup.rejected_by = user
        dup.save()

    print(f"🔥 Rejected {duplicates.count()} duplicate complaints")

    # --------------------------------------------------
    # 🚫 USER BLOCKING LOGIC
    # --------------------------------------------------
    complaint_user = grievance.user

    rejected_count = Grievance.objects.filter(
        user=complaint_user,
        status="rejected"
    ).count()

    user_blocked = False

    if rejected_count >= MAX_REJECTION_LIMIT:
        complaint_user.is_blocked = True
        complaint_user.save()
        user_blocked = True

    # --------------------------------------------------
    # 📦 RESPONSE
    # --------------------------------------------------
    return {
        "rejected_count": rejected_count,
        "user_blocked": user_blocked
    }