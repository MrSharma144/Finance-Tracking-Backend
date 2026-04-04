from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ADMIN = 'Admin'
    ANALYST = 'Analyst'
    VIEWER = 'Viewer'
    
    ROLE_CHOICES = [
        (ADMIN, 'Admin'),
        (ANALYST, 'Analyst'),
        (VIEWER, 'Viewer'),
    ]
    
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default=VIEWER
    )

    def __str__(self):
        return f"{self.username} ({self.role})"
