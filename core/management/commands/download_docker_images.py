import subprocess

from django.core.management.base import BaseCommand


def download_docker_images(self):
    images = ["gcc:12", "node:20.10.0-alpine", "eclipse-temurin:11", "python:alpine"]
    for img in images:
        try:
            result = subprocess.run(
                ["docker", "pull", img],
                shell=False,
                check=True,
            )
            if result:
                self.stdout.write(self.style.SUCCESS(f"Image {img} Downloaded"))
        except subprocess.CalledProcessError:
            self.stdout.write(self.style.ERROR("Error!!!"))


class Command(BaseCommand):
    help = "Download Docker Images"

    def handle(self, *args, **options):
        download_docker_images(self)
        self.stdout.write(self.style.SUCCESS("Successfully"))
