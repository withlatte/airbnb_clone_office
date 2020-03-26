from django.core.management.base import BaseCommand
from django_seed import Seed
from users.models import User


class Command(BaseCommand):
    help = "Seed Users (feat. django-seed & faker)"

    def add_arguments(self, parser):
        parser.add_argument(
            "--times",
            type=int,
            default=1,
            help="This will seed users testing data n times.",
        )

    def handle(self, *args, **options):
        how_many = options["times"]
        seeder = Seed.seeder()

        seeder.add_entity(
            User,
            how_many,
            {
                "is_superuser": lambda x: False,
                "is_staff": lambda x: False,
                "avatar": lambda x: False,
            },
        )

        seeder.execute()

        self.stdout.write(
            self.style.NOTICE(f"{how_many} users are successfully seeded!")
        )
