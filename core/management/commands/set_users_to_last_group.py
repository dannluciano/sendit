from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import Group, User


class Command(BaseCommand):
    help = "Set Users without Group to the last created Group"

    def handle(self, *args, **options):
        last_group = Group.objects.last()
        users = User.objects.all()

        for u in users:
            if not u.groups.all():
                u.groups.set([last_group])
                u.save()

        self.stdout.write(self.style.SUCCESS("Successfully"))
