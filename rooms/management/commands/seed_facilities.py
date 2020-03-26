from django.core.management.base import BaseCommand
from rooms.models import Facility


class Command(BaseCommand):
    help = "Seed Facilities"

    # def add_arguments(self, parser):
    #     parser.add_argument(
    #         "--times", type=int, help="This will seed amenities testing data n times."
    #     )

    def handle(self, *args, **options):
        # how_many = options["times"]
        facilities = [
            "Private entrance",
            "Paid parking on premises",
            "Paid parking off premises",
            "Elevator",
            "Parking",
            "Gym",
        ]
        for n in facilities:
            Facility.objects.create(name=n)

        self.stdout.write(self.style.NOTICE(f"Facilities are successfully seeded!"))
