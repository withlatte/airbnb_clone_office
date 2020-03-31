from django.shortcuts import render
from . import models as room_models


def all_rooms(request):
    all_my_rooms = room_models.Room.objects.all()
    page_size = 10
    page_num = request.GET.get("page")
    page_num = int(page_num)
    limits = page_size * page_num
    offset = limits - page_size
    limited_my_rooms = all_my_rooms[offset:limits]

    return render(
        request, "rooms/home.html", context={"all_my_rooms": limited_my_rooms}
    )
