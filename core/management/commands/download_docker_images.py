import docker
from django.core.management.base import BaseCommand


def download_docker_images(self):
    dockercli = docker.from_env()
    images = [
        "gcc:15",
        "node:24.13.1-alpine",
        "eclipse-temurin:21",
        "python:3.14-alpine",
    ]
    for img in images:
        try:
            dockercli.images.pull(img)
            self.stdout.write(self.style.SUCCESS(f"Image {img} Downloaded"))

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"Error downloading image {img}: {e}")
            )


class Command(BaseCommand):
    help = "Download Docker Images"

    def handle(self, *args, **options):
        download_docker_images(self)
        self.stdout.write(self.style.SUCCESS("Successfully"))
