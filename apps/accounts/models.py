

from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('CITIZEN', 'Citizen'),
        ('OFFICER', 'Officer'),
        ('ADMIN', 'Admin'),
    )

    DEPT_CHOICES = (
        ('ROAD', 'Road'),
        ('WATER', 'Water'),
        ('LIGHT', 'Light'),
        ('SEWAGE', 'Sewage'),
        ('GARBAGE', 'Garbage'),
    )

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='CITIZEN'
    )

    department = models.CharField(
        max_length=10,
        choices=DEPT_CHOICES,
        null=True,
        blank=True
    )

    mobile = models.CharField(
        max_length=10,
        unique=True,
        null=True,
        blank=True
    )


    def __str__(self):
        return f"{self.username} ({self.role})"
