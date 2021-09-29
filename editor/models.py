import uuid
from django.db import models
from django.contrib.auth.models import User
from core.models import Submission
from django.urls import reverse


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


class FileCode(models.Model):
    uuid = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        editable=False
    )

    name = models.CharField(
        max_length=255
    )

    code = models.TextField()

    language = models.CharField(
        choices=Submission.LANGUAGE_CHOICES,
        default=Submission.LANGUAGE_CHOICES[0][0],
        max_length=10
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="owner_file_code"
    )

    def __str__(self):
        return f"{self.uuid} - {self.language} - {self.owner}"

    def get_absolute_url(self):
        return reverse("editor:file-code-detail", kwargs={"file_code_uuid": self.uuid})
    
