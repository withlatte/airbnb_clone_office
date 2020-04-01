from django.shortcuts import render
from django.utils import timezone
from django.views.generic import ListView
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


def room_detail(request, pk):
    return render(request, "rooms/detail.html")


"""
def all_rooms(request):
    all_my_rooms = room_models.Room.objects.all()

    page_num = request.GET.get("page")
    paginator = Paginator(all_my_rooms, 10, orphans=5)
    room = paginator.get_page(page_num)

    return render(request, "rooms/home.html", context={"all_my_rooms": room,},)
"""
