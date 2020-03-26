from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "I LOVE YOU MACHINE"

    def add_arguments(self, parser):
        parser.add_argument(
            "--times", type=int, help="I will say loud, I LOVE YOU n times."
        )

    def handle(self, *args, **options):
        how_many = options["times"]

        for n in range(how_many):
            self.stdout.write(self.style.NOTICE("I LOVE YOU"))
