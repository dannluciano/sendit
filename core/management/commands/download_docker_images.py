import multiprocessing

import docker
from django.core.management.base import BaseCommand

from core.submission_runner import IMAGE_VERSION_DICT


def download_docker_images(self):
    images = IMAGE_VERSION_DICT.values()

    with multiprocessing.Pool(processes=len(images)) as pool:
        pool.map(pull_image, images)


def pull_image(image_name):
    try:
        dockercli = docker.from_env()
        dockercli.images.pull(image_name)
    except Exception as e:
        print(f"Error pulling image {image_name}: {e}")


class Command(BaseCommand):
    help = "Download Docker Images"

    def handle(self, *args, **options):
        download_docker_images(self)
        self.stdout.write(self.style.SUCCESS("Successfully"))
