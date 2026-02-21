


from django.contrib.gis.db import models
from django.conf import settings
from django.utils import timezone


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

    # 👤 Citizen who created grievance
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="grievances"
    )

    # 👮 Assigned Officer
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_grievances"
    )

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    # 🏢 Department (AI detected or manual)
    department = models.CharField(
        max_length=100,
        default="Pending"
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

    # 🧠 AI fields
    image = models.ImageField(upload_to="grievances/", null=True, blank=True)

    detected_issue = models.CharField(
        max_length=50,
        null=True,
        blank=True
    )

    ai_confidence = models.FloatField(
        null=True,
        blank=True
    )

    # ⏳ Time tracking (VERY IMPORTANT for dashboard)
    created_at = models.DateTimeField(auto_now_add=True)

    resolved_at = models.DateTimeField(
        null=True,
        blank=True
    )


        # 🚨 Escalation fields
    is_escalated = models.BooleanField(default=False)

    escalated_at = models.DateTimeField(
        null=True,
        blank=True
    )


    def mark_as_resolved(self):
        self.status = "resolved"
        self.resolved_at = timezone.now()
        self.save()

    def __str__(self):
        return f"{self.title} - {self.status}"

