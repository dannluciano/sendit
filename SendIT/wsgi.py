"""
WSGI config for SendIT project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import logging
import os
import subprocess

from django.db.backends.signals import connection_created
from django.dispatch import receiver

log = logging.getLogger("SendIT")
log.setLevel(logging.INFO)


@receiver(connection_created)
def setup_postgres(connection, **kwargs):
    if connection.vendor != "postgresql":
        return

    # Timeout statements after 20 seconds.
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SET statement_timeout TO 20000;
        """
        )


def create_virtual_env():
    if not os.path.exists("worker_env"):
        try:
            result = subprocess.run(
                ["python", "-m", "venv", "worker_env"],
                shell=False,
                check=True,
                timeout=5,
            )
            
            if result:
                log.info("Virtual Env Created")
        except subprocess.TimeoutExpired:
            log.error("TimeOut! Virtual Env isn't created!!!")
        except subprocess.CalledProcessError:
            pass


create_virtual_env()

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SendIT.settings")

application = get_wsgi_application()
