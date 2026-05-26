import uuid

from django.core.validators import RegexValidator
from django.db import models

safe_project_name_validator = RegexValidator(
    regex=r"^[A-Za-z0-9_-]+\Z",
    message="Use apenas letras, numeros, underscore e hifen.",
)


class Project(models.Model):
    name = models.CharField(
        "Nome",
        max_length=100,
        unique=False,
        validators=[safe_project_name_validator],
    )

    owner = models.ForeignKey(
        "auth.User",
        verbose_name="Dono",
        on_delete=models.CASCADE,
    )

    container_id = models.CharField(
        max_length=250,
        blank=True,
    )

    created_at = models.DateTimeField(
        "Criado em",
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        "Atualizado em",
        auto_now=True,
    )

    uuid = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        editable=False,
    )

    def __str__(self) -> str:
        return f"{self.owner} - {self.name}"

    @property
    def get_temp_dir(self):
        return f"{self.uuid}"

    def to_dict(self):
        return {
            "uuid": str(self.uuid),
            "name": self.name,
            "owner_id": self.owner_id,
            "temp_dir": self.get_temp_dir,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["name", "owner"], name="unique_project_name_by_owner"
            ),
        ]
