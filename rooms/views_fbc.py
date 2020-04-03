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

    country = request.GET.get("country", "KR")

    room_type = request.GET.get("room_type", 0)
    room_type = int(room_type)

    price = request.GET.get("price", 0)
    price = int(price)

    guests = request.GET.get("guests", 0)
    guests = int(guests)

    beds = request.GET.get("beds", 0)
    beds = int(beds)

    bedrooms = request.GET.get("bedrooms", 0)
    bedrooms = int(bedrooms)

    baths = request.GET.get("baths", 0)
    baths = int(baths)

    s_amenities = request.GET.getlist("amenities")  # getlist ATTENTION
    s_facilities = request.GET.getlist("facilities")
    s_instant = bool(request.GET.get("instant", False))
    s_super_host = bool(request.GET.get("super_host", False))

    form = {
        "city": city,
        "s_country": country,
        "s_room_type": room_type,
        "s_price": price,
        "s_guest": guests,
        "s_bed": beds,
        "s_bedroom": bedrooms,
        "s_bath": baths,
        "s_amenities": s_amenities,
        "s_facilities": s_facilities,
        "instant": s_instant,
        "super_host": s_super_host,
    }

    room_types = room_models.RoomType.objects.all()
    amenities = room_models.Amenity.objects.all()
    facilities = room_models.Facility.objects.all()

    choices = {
        "countries": countries,
        "room_types": room_types,
        "amenities": amenities,
        "facilities": facilities,
    }

    filter_args = {}

    if city != "Anywhere":
        filter_args["city__startswith"] = city

    filter_args["country"] = country

    if room_type != 0:
        filter_args["room_type__pk"] = room_type

    if price != 0:
        filter_args["price__lte"] = price

    if guests != 0:
        filter_args["guests__gte"] = guests

    if beds != 0:
        filter_args["beds__lte"] = beds

    if bedrooms != 0:
        filter_args["bedrooms__lte"] = bedrooms

    if baths != 0:
        filter_args["baths__lte"] = baths

    if s_instant:
        filter_args["instant_book"] = True

    if s_super_host:
        filter_args["host__super_host"] = True

    if len(s_amenities) > 0:
        for s_amenity in s_amenities:
            filter_args["amenities__pk"] = int(s_amenity)

    if len(s_facilities) > 0:
        for s_facility in s_facilities:
            filter_args["facilities__pk"] = int(s_facility)

    rooms = room_models.Room.objects.filter(**filter_args)

    return render(request, "rooms/search.html", {**form, **choices, "rooms": rooms},)


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
