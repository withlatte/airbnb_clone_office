from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils import timezone
from django.shortcuts import render, redirect, reverse
from django.views.generic import (
    ListView,
    DetailView,
    View,
    UpdateView,
    FormView,
    DeleteView,
)
from django.core.paginator import Paginator
from users import mixins as user_mixins
from . import models as room_models
from . import forms as forms


class HomeView(ListView):
    """ Home View Definition """

    model = room_models.Room
    context_object_name = "room_obj_list"
    paginate_by = 12
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
            form = forms.SearchForm(request.GET)

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
            form = forms.SearchForm()

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


class EditRoomView(user_mixins.LoggedInOnlyView, UpdateView):
    """ Edit Room View Definition """

    model = room_models.Room
    template_name = "rooms/room_edit.html"

    fields = (
        "name",
        "description",
        "country",
        "city",
        "address",
        "price",
        "guests",
        "beds",
        "bedrooms",
        "baths",
        "check_in",
        "check_out",
        "instant_book",
        "room_type",
        "amenities",
        "facilities",
        "house_rules",
    )

    def get_object(self, queryset=None):
        room = super(EditRoomView, self).get_object()
        if room.host.pk != self.request.user.pk:
            raise Http404()
        else:
            return room


class RoomPhotosView(user_mixins.LoggedInOnlyView, DetailView):
    """ Room Photos View Definition """

    model = room_models.Room
    template_name = "rooms/room_photos.html"

    def get_object(self, queryset=None):
        room = super(RoomPhotosView, self).get_object()
        if room.host.pk != self.request.user.pk:
            raise Http404()
        else:
            return room


@login_required
def delete_photo(request, room_pk, photo_pk):
    user = request.user
    try:
        room = room_models.Room.objects.get(pk=room_pk)
        if room.host.pk != user.pk:
            messages.error(request, "You are not allowed to delete this photo.")
        else:
            room_models.Photo.objects.filter(pk=photo_pk).delete()
            messages.success(request, "사진이 삭제되었습니다")
        return redirect(reverse("rooms:photos", kwargs={"pk": room_pk}))
    except room_models.Room.DoesNotExist:
        return redirect(reverse("core:home"))


class DeletePhotoView(user_mixins.LoggedInOnlyView, DeleteView):
    """ Delete Photo View Definition """

    model = room_models.Photo
    pk_url_kwarg = "photo_pk"

    def get_success_url(self):
        room_pk = self.kwargs.get("room_pk")
        messages.success(self.request, "사진이 삭제되었습니다")
        return reverse("rooms:photos", kwargs={"pk": room_pk})


class EditPhotoView(user_mixins.LoggedInOnlyView, UpdateView):
    """ Edit Photo View """

    model = room_models.Photo
    template_name = "rooms/photo_edit.html"
    pk_url_kwarg = "photo_pk"
    fields = ("caption",)

    def get_success_url(self):
        room_pk = self.kwargs.get("room_pk")
        messages.success(self.request, "사진설명이 변경되었습니다")
        return reverse("rooms:photos", kwargs={"pk": room_pk})


class AddPhotoView(user_mixins.LoggedInOnlyView, FormView):
    """ Add Photo View Definition """

    model = room_models.Photo
    template_name = "rooms/photo_create.html"
    form_class = forms.CreatePhotoForm

    def form_valid(self, form):
        pk = self.kwargs.get("pk")
        form.save(pk)
        messages.success(self.request, "Photo has been added successfully")
        return redirect(reverse("rooms:photos", kwargs={"pk": pk}))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["room_pk"] = self.kwargs.get("pk")
        return context
