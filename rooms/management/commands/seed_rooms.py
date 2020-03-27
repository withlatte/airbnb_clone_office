import random
from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed
from rooms import models as room_models
from users import models as user_models


class Command(BaseCommand):
    help = "Seed Rooms (feat. django-seed & faker)"

    def add_arguments(self, parser):
        parser.add_argument(
            "--times",
            type=int,
            default=1,
            help="This will seed rooms and room photos testing data n times.",
        )

    def handle(self, *args, **options):
        how_many = options["times"]
        seeder = Seed.seeder()

        all_user = user_models.User.objects.all()
        amenities = room_models.Amenity.objects.all()
        facilities = room_models.Facility.objects.all()
        rules = room_models.HouseRule.objects.all()
        room_types = room_models.RoomType.objects.all()

        seeder.add_entity(
            room_models.Room,
            how_many,
            {
                "name": lambda x: seeder.faker.address(),
                "address": lambda x: seeder.faker.address(),
                "host": lambda x: random.choice(all_user),
                "room_type": lambda x: random.choice(room_types),
                "guests": lambda x: random.randint(0, 30),
                "price": lambda x: random.randint(1, 300),
                "beds": lambda x: random.randint(1, 20),
                "bedrooms": lambda x: random.randint(1, 10),
                "baths": lambda x: random.randint(1, 10),
            },
        )
        created_photos = (
            seeder.execute()
        )  # DB에 저장 후 Dictionary type 으로 {class : primary key}로 리턴
        created_clean = flatten(list(created_photos.values()))  # 위 Dict pk 값을 List 로 전환
        for pk in created_clean:
            room = room_models.Room.objects.get(pk=pk)
            for i in range(1, random.randint(3, 30)):
                room_models.Photo.objects.create(
                    caption=seeder.faker.sentence(),
                    room=room,
                    file=f"room_photos/{random.randint(1, 31)}.webp",
                )
            for a in amenities:
                magic_number = random.randint(0, 15)
                if magic_number % 2 == 0:
                    room.amenities.add(a)

            for f in facilities:
                magic_number = random.randint(0, 15)
                if magic_number % 2 == 0:
                    room.facilities.add(f)

            for r in rules:
                magic_number = random.randint(0, 15)
                if magic_number % 2 == 0:
                    room.house_rules.add(r)

        self.stdout.write(
            self.style.NOTICE(f"{how_many} rooms are successfully seeded!")
        )
