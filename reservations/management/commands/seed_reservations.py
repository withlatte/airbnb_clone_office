import random
from django.core.management.base import BaseCommand
from django_seed import Seed
from rooms import models as room_models
from users import models as user_models
from reservations import models as reservation_models

NAME = "reservations"


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
            reservation_models.Reservation,
            how_many,
            {
                # "status": lambda x: random.choice(),
                "check_in": lambda x: seeder.faker.date_between(
                    start_date="+1d", end_date="+20d"
                ),
                "check_out": lambda x: seeder.faker.date_between(
                    start_date="+21d", end_date="+40d"
                ),
                "guest": lambda x: random.choice(all_user),
                "room": lambda x: random.choice(all_room),
            },
        )
        seeder.execute()

        self.stdout.write(
            self.style.NOTICE(f"{how_many} {NAME} are successfully seeded!")
        )
