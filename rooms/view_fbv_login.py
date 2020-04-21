from django.urls import reverse

# from django.http import Http404
from django.utils import timezone
from django.shortcuts import render
from django.views.generic import ListView, DetailView, View
from django.core.paginator import Paginator
from django_countries import countries
from . import models as room_models
from . import forms as search_forms


class HomeView(ListView):
    """ Home View Definition """

    model = room_models.Room
    context_object_name = "room_obj_list"
    paginate_by = 10
    paginate_orphans = 5
    template_name = "rooms/room_list.html"

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


class SearchView(View):
    """ Search View Definition """

    def get(self, request):

        country = request.GET.get("country")

        if country:
            form = search_forms.SearchForm(request.GET)

            if form.is_valid():
                city = form.cleaned_data.get("city")
                country = form.cleaned_data.get("country")
                room_type = form.cleaned_data.get("room_type")
                price = form.cleaned_data.get("price")
                guests = form.cleaned_data.get("guests")
                beds = form.cleaned_data.get("beds")
                bedrooms = form.cleaned_data.get("bedrooms")
                baths = form.cleaned_data.get("baths")
                instant_book = form.cleaned_data.get("instant_book")
                super_host = form.cleaned_data.get("super_host")
                amenities = form.cleaned_data.get("amenities")
                facilities = form.cleaned_data.get("facilities")

                filter_args = {}

                if city != "Anywhere":
                    filter_args["city__startswith"] = city

                filter_args["country"] = country

                if room_type is not None:
                    filter_args["room_type__pk"] = room_type

                if price is not None:
                    filter_args["price__lte"] = price

                if guests is not None:
                    filter_args["guests__gte"] = guests

                if beds is not None:
                    filter_args["beds__lte"] = beds

                if bedrooms is not None:
                    filter_args["bedrooms__lte"] = bedrooms

                if baths is not None:
                    filter_args["baths__lte"] = baths

                if instant_book:
                    filter_args["instant_book"] = True

                if super_host:
                    filter_args["host__super_host"] = True

                for amenity in amenities:
                    filter_args["amenities"] = amenity

                for facility in facilities:
                    filter_args["facilities"] = facility

                qs = room_models.Room.objects.filter(**filter_args).order_by("-created")
                paginator = Paginator(qs, 10, orphans=5)
                page = request.GET.get("page", 1)
                rooms = paginator.get_page(page)

                return render(
                    request, "rooms/search.html", {"form": form, "rooms": rooms},
                )
        else:
            form = search_forms.SearchForm()

        return render(request, "rooms/search.html", {"form": form},)


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

    return render(request, "rooms/room_list.html", context={"all_my_rooms": room,},)
"""
