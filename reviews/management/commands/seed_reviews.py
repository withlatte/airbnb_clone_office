import random
from django.core.management.base import BaseCommand

# from django.contrib.admin.utils import flatten
from django_seed import Seed
from rooms import models as room_models
from users import models as user_models
from reviews import models as review_models

NAME = "reviews"


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
            review_models.Review,
            how_many,
            {
                "accuracy": lambda x: random.randint(0, 5),
                "communication": lambda x: random.randint(0, 5),
                "cleanliness": lambda x: random.randint(0, 5),
                "location": lambda x: random.randint(0, 5),
                "check_in": lambda x: random.randint(0, 5),
                "value": lambda x: random.randint(0, 5),
                "user": lambda x: random.choice(all_user),
                "room": lambda x: random.choice(all_room),
            },
        )
        seeder.execute()

        self.stdout.write(
            self.style.NOTICE(f"{how_many} {NAME} are successfully seeded!")
        )
