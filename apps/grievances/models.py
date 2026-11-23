



# from django.contrib.gis.db import models
# from django.conf import settings
# from django.utils import timezone
# from apps.departments.models import Department

# # ======================================================
# # MAIN GRIEVANCE MODEL
# # ======================================================

# class Grievance(models.Model):

#     STATUS_CHOICES = (
#         ('pending', 'Pending'),
#         ('assigned', 'Assigned'),
#         ('in_progress', 'In Progress'),
#         ('resolved', 'Resolved'),
#         ('rejected', 'Rejected'),
#         ('escalated', 'Escalated'),
#     )

#     PRIORITY_CHOICES = (
#         ("LOW", "Low"),
#         ("MEDIUM", "Medium"),
#         ("HIGH", "High"),
#         ("CRITICAL", "Critical"),
#     )

#     # 👤 Citizen who created grievance
#     user = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE,
#         related_name="grievances"
#     )

#     # 👮 Assigned Officer (optional main officer)
#     assigned_to = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.SET_NULL,
#         null=True,
#         blank=True,
#         related_name="assigned_grievances"
#     )

#     title = models.CharField(max_length=255)
#     description = models.TextField(blank=True)

#     # 🏢 Departments (AI detected)
#     department = models.ManyToManyField(
#         Department,
#         blank=True,
#         related_name="grievances"
#     )

#     priority = models.CharField(
#         max_length=10,
#         choices=PRIORITY_CHOICES,
#         default="LOW"
#     )

#     location = models.PointField()

#     status = models.CharField(
#         max_length=20,
#         choices=STATUS_CHOICES,
#         default="pending"
#     )

#     # 📸 Citizen Complaint Image
#     image = models.ImageField(
#         upload_to="grievances/complaints/",
#         null=True,
#         blank=True
#     )

#     # 🧠 AI detection fields
#     detected_issue = models.CharField(
#         max_length=255,
#         null=True,
#         blank=True
#     )

#     ai_confidence = models.FloatField(
#         null=True,
#         blank=True
#     )

#     # 📸 Proof Images (for single department cases)
#     before_image = models.ImageField(
#         upload_to="grievances/proof/before/",
#         null=True,
#         blank=True
#     )

#     after_image = models.ImageField(
#         upload_to="grievances/proof/after/",
#         null=True,
#         blank=True
#     )

#     # 📝 Resolution note
#     resolution_note = models.TextField(
#         null=True,
#         blank=True
#     )

#     # 👮 Who resolved the complaint
#     resolved_by = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.SET_NULL,
#         null=True,
#         blank=True,
#         related_name="resolved_grievances"
#     )

#     # 🚫 Rejection System (NEW FEATURE)
#     rejection_proof = models.ImageField(
#         upload_to="grievances/rejection_proof/",
#         null=True,
#         blank=True
#     )

#     rejection_reason = models.TextField(
#         null=True,
#         blank=True
#     )

#     rejected_by = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.SET_NULL,
#         null=True,
#         blank=True,
#         related_name="rejected_grievances"
#     )

#     # ⏳ Time tracking
#     created_at = models.DateTimeField(auto_now_add=True)

#     resolved_at = models.DateTimeField(
#         null=True,
#         blank=True
#     )

#     # 🚨 Escalation fields
#     is_escalated = models.BooleanField(default=False)

#     escalated_at = models.DateTimeField(
#         null=True,
#         blank=True
#     )

#     # --------------------------------------------------
#     # Update grievance status based on department tasks
#     # --------------------------------------------------

#     def update_status_from_departments(self):
#         tasks = self.department_tasks.all()

#         if not tasks.exists():
#             return

#         if all(task.status == "resolved" for task in tasks):
#             self.status = "resolved"
#             self.resolved_at = timezone.now()
#         else:
#             self.status = "in_progress"

#         self.save()

#     def mark_as_resolved(self, officer=None):
#         self.status = "resolved"
#         self.resolved_at = timezone.now()
#         self.resolved_by = officer
#         self.save()

#     def __str__(self):
#         return f"{self.title} - {self.status}"


# # ======================================================
# # DEPARTMENT LEVEL TASK MODEL
# # ======================================================

# class GrievanceDepartmentTask(models.Model):

#     STATUS_CHOICES = (
#         ("pending", "Pending"),
#         ("in_progress", "In Progress"),
#         ("resolved", "Resolved"),
#     )

#     grievance = models.ForeignKey(
#         Grievance,
#         on_delete=models.CASCADE,
#         related_name="department_tasks"
#     )

#     department = models.ForeignKey(
#         Department,
#         on_delete=models.CASCADE
#     )

#     officer = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.SET_NULL,
#         null=True,
#         blank=True
#     )

#     status = models.CharField(
#         max_length=20,
#         choices=STATUS_CHOICES,
#         default="pending"
#     )

#     # 📸 Department specific proof images
#     before_image = models.ImageField(
#         upload_to="grievances/department_proof/before/",
#         null=True,
#         blank=True
#     )

#     after_image = models.ImageField(
#         upload_to="grievances/department_proof/after/",
#         null=True,
#         blank=True
#     )

#     resolution_note = models.TextField(
#         null=True,
#         blank=True
#     )

#     resolved_at = models.DateTimeField(
#         null=True,
#         blank=True
#     )

#     created_at = models.DateTimeField(auto_now_add=True)

#     def mark_resolved(self):
#         self.status = "resolved"
#         self.resolved_at = timezone.now()
#         self.save()

#         # update parent grievance automatically
#         self.grievance.update_status_from_departments()

#     def __str__(self):
#         return f"Grievance {self.grievance.id} - {self.department.name}"


# # ======================================================
# # 🆕 OFFICER ACTION MODEL (NEW FEATURE)
# # ======================================================

# class OfficerAction(models.Model):

#     ACTION_CHOICES = [
#         ("WARNING", "Warning"),
#         ("REASSIGN", "Reassign"),
#     ]

#     grievance = models.ForeignKey(
#         Grievance,
#         on_delete=models.CASCADE,
#         related_name="officer_actions"
#     )

#     officer = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE
#     )

#     action_type = models.CharField(
#         max_length=20,
#         choices=ACTION_CHOICES
#     )

#     reason = models.TextField()

#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.action_type} - {self.officer}"

from django.contrib.gis.db import models
from django.conf import settings
from django.utils import timezone
from apps.departments.models import Department

User = settings.AUTH_USER_MODEL


# ======================================================
# MAIN GRIEVANCE MODEL
# ======================================================

class Grievance(models.Model):

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('assigned', 'Assigned'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('rejected', 'Rejected'),
        ('escalated', 'Escalated'),
    )

    PRIORITY_CHOICES = (
        ("LOW", "Low"),
        ("MEDIUM", "Medium"),
        ("HIGH", "High"),
        ("CRITICAL", "Critical"),
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="grievances"
    )

    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_grievances"
    )

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    department = models.ManyToManyField(
        Department,
        blank=True,
        related_name="grievances"
    )

    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default="LOW"
    )

    location = models.PointField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )

    image = models.ImageField(
        upload_to="grievances/complaints/",
        null=True,
        blank=True
    )

    detected_issue = models.CharField(max_length=255, null=True, blank=True)
    ai_confidence = models.FloatField(null=True, blank=True)

    # ================= DUPLICATE =================

    is_duplicate = models.BooleanField(default=False)

    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="duplicates"
    )

    linked_users = models.ManyToManyField(
        User,
        related_name="linked_grievances",
        blank=True
    )

    text_embedding = models.JSONField(null=True, blank=True)
    image_embedding = models.JSONField(null=True, blank=True)

    # ================= PROOF =================

    before_image = models.ImageField(
        upload_to="grievances/proof/before/",
        null=True,
        blank=True
    )

    after_image = models.ImageField(
        upload_to="grievances/proof/after/",
        null=True,
        blank=True
    )

    resolution_note = models.TextField(null=True, blank=True)

    resolved_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="resolved_grievances"
    )

    rejection_proof = models.ImageField(
        upload_to="grievances/rejection_proof/",
        null=True,
        blank=True
    )

    rejection_reason = models.TextField(null=True, blank=True)

    rejected_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="rejected_grievances"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    resolved_at = models.DateTimeField(null=True, blank=True)

    is_escalated = models.BooleanField(default=False)
    escalated_at = models.DateTimeField(null=True, blank=True)

    # ======================================================
    # 🔁 STATUS LOGIC (FINAL FIX)
    # ======================================================

    def update_status_from_departments(self):
        tasks = self.department_tasks.all()

        if not tasks.exists():
            return

        if all(task.status == "resolved" for task in tasks):
            self.status = "resolved"
            self.resolved_at = timezone.now()
        else:
            self.status = "in_progress"

        self.save()

        # 🔥 SYNC RESOLVED TO DUPLICATES
        if self.status == "resolved":
            duplicates = self.duplicates.all()

            for dup in duplicates:
                dup.status = "resolved"
                dup.resolved_at = self.resolved_at
                dup.resolution_note = self.resolution_note
                dup.department.set(self.department.all())
                dup.save()

            print(f"🔥 Synced {duplicates.count()} resolved duplicates")

    # ======================================================
    # 🔥 NEW: REJECTION SYNC METHOD
    # ======================================================

    def sync_rejection_to_duplicates(self):
        duplicates = self.duplicates.all()

        for dup in duplicates:
            dup.status = "rejected"
            dup.rejection_reason = self.rejection_reason
            dup.rejection_proof = self.rejection_proof
            dup.rejected_by = self.rejected_by
            dup.save()

        print(f"🔥 Synced {duplicates.count()} rejected duplicates")

    def mark_as_resolved(self, officer=None):
        self.status = "resolved"
        self.resolved_at = timezone.now()
        self.resolved_by = officer
        self.save()

    def get_total_reports(self):
        if self.is_duplicate and self.parent:
            return self.parent.linked_users.count()
        return self.linked_users.count()

    def __str__(self):
        return f"{self.title} - {self.status}"


# ======================================================
# DEPARTMENT LEVEL TASK MODEL
# ======================================================

class GrievanceDepartmentTask(models.Model):

    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("in_progress", "In Progress"),
        ("resolved", "Resolved"),
    )

    grievance = models.ForeignKey(
        Grievance,
        on_delete=models.CASCADE,
        related_name="department_tasks"
    )

    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE
    )

    officer = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )

    before_image = models.ImageField(
        upload_to="grievances/department_proof/before/",
        null=True,
        blank=True
    )

    after_image = models.ImageField(
        upload_to="grievances/department_proof/after/",
        null=True,
        blank=True
    )

    resolution_note = models.TextField(null=True, blank=True)

    resolved_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def mark_resolved(self):
        self.status = "resolved"
        self.resolved_at = timezone.now()
        self.save()

        self.grievance.update_status_from_departments()

    def __str__(self):
        return f"Grievance {self.grievance.id} - {self.department.name}"


# ======================================================
# OFFICER ACTION MODEL
# ======================================================

class OfficerAction(models.Model):

    ACTION_CHOICES = [
        ("WARNING", "Warning"),
        ("REASSIGN", "Reassign"),
    ]

    grievance = models.ForeignKey(
        Grievance,
        on_delete=models.CASCADE,
        related_name="officer_actions"
    )

    officer = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    action_type = models.CharField(
        max_length=20,
        choices=ACTION_CHOICES
    )

    reason = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.action_type} - {self.officer}"