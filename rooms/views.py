from django.urls import reverse

# from django.http import Http404
from django.utils import timezone
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django_countries import countries
from . import models as room_models


class HomeView(ListView):
    """ Home View Definition """

    model = room_models.Room
    context_object_name = "room_obj_list"
    paginate_by = 10
    paginate_orphans = 5
    template_name = "rooms/home.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.now()
        context["now"] = now
        return context


class RoomDetailView(DetailView):
    """ Room Detail View Definition """

    # DetailView names "context_obj_name" to name of model which is "Room".
    # it turns "Room" to small letters "room" and then use it by default.
    model = room_models.Room


def search(request):
    city = request.GET.get("city", "Anywhere")
    city = str.capitalize(city)
    room_types = room_models.RoomType.objects.all()

    return render(
        request,
        "rooms/search.html",
        {"city": city, "countries": countries, "room_types": room_types},
    )


"""
def room_detail(request, pk):
    try:
        room = room_models.Room.objects.get(pk=pk)
        return render(request, "rooms/room_detail.html", {"room": room})
    except room_models.Room.DoesNotExist:
        raise Http404()
        # return redirect(reverse("core:home"))

def all_rooms(request):
    all_my_rooms = room_models.Room.objects.all()

    page_num = request.GET.get("page")
    paginator = Paginator(all_my_rooms, 10, orphans=5)
    room = paginator.get_page(page_num)

    return render(request, "rooms/home.html", context={"all_my_rooms": room,},)
"""
