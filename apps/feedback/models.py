

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone

from apps.accounts.models import User
from apps.grievances.models import Grievance
from django.conf import settings


class Feedback(models.Model):

    grievance = models.OneToOneField(
        Grievance,
        on_delete=models.CASCADE,
        related_name="feedback"
    )

    # 👮 Store officer directly (faster dashboard queries)
    officer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="received_feedbacks"
    )

    rating = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ]
    )

    comment = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Auto-assign officer from grievance
        if self.grievance and not self.officer:
            self.officer = self.grievance.assigned_to

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Feedback - Grievance #{self.grievance.id} - Rating {self.rating}"
