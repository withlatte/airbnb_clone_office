import random
from django.core.management.base import BaseCommand

from django.contrib.admin.utils import flatten
from django_seed import Seed
from rooms import models as room_models
from users import models as user_models
from lists import models as list_models

NAME = "lists"


class Command(BaseCommand):
    help = f"Seed {NAME} (feat. django-seed & faker)"

    def add_arguments(self, parser):
        parser.add_argument(
            "--times",
            type=int,
            default=1,
            help=f"This will seed {NAME} testing data n times.",
        )

    def handle(self, *args, **options):
        how_many = options["times"]
        seeder = Seed.seeder()

        all_user = user_models.User.objects.all()
        all_room = room_models.Room.objects.all()

        seeder.add_entity(
            list_models.List, how_many, {"user": lambda x: random.choice(all_user),},
        )

        # Seeding in to ManyToMany Fields
        created = seeder.execute()  # seeder.execute() returns Dictionary Type of values
        cleaned = flatten(
            list(created.values())  # make list of created values of Dictionary
        )
        for pk in cleaned:
            list_model = list_models.List.objects.get(pk=pk)
            to_add = all_room[random.randint(0, 5) : random.randint(6, 30)]
            list_model.rooms.add(*to_add)

        self.stdout.write(
            self.style.NOTICE(f"{how_many} {NAME} are successfully seeded!")
        )
