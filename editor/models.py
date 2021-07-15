import uuid
from django.db import models
from core.models import Submission

class Runner(models.Model):
    uuid = models.UUIDField(
        unique=True, 
        default=uuid.uuid4, 
        editable=False
    )
    
    code = models.TextField()

    status = models.CharField(
        choices=Submission.STATUS_CHOICES, 
        default=Submission.STATUS_CHOICES[0][0], 
        max_length=255
    )

    language = models.CharField(
        choices=Submission.LANGUAGE_CHOICES, 
        default=Submission.LANGUAGE_CHOICES[0][0],
        max_length=10
    )

    log = models.TextField(
        blank=True
    )

    input = models.TextField(
        blank=True
    )

    output = models.TextField(
        blank=True
    )

    timestamp = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.uuid} - {self.language} - {self.timestamp}"