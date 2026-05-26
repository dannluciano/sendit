from django.core.files.base import ContentFile
from django.core.files.storage import storages
from django.db import migrations


def migrate_badges_to_s3(apps, schema_editor):
    Achievement = apps.get_model("core", "Achievement")
    AchievementPicture = apps.get_model("core", "AchievementPicture")

    print("Starting migrate badges to s3...")
    for achievement in Achievement.objects.all():
        file_name = achievement.badge.file.filename
        file_bytes = achievement.badge.file.read()
        file_type = achievement.badge.file.mimetype

        print(f"Migrating {file_name} with MIME {file_type} to S3")

        content = ContentFile(file_bytes, name=file_name)
        content.content_type = file_type

        achievement.badge_s3 = storages["s3"].save(file_name, content)
        achievement.save(update_fields=["badge_s3"])


def reverse_badges_from_s3(apps, schema_editor):
    Achievement = apps.get_model("core", "Achievement")
    for achievement in Achievement.objects.all():
        achievement.badge_s3 = ""
        achievement.save(update_fields=["badge_s3"])


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0016_achievement_badge_s3"),
    ]

    operations = [
        migrations.RunPython(
            migrate_badges_to_s3,
            reverse_code=reverse_badges_from_s3,
        ),
    ]
