from django.urls import path
from . import views as room_views

app_name = "rooms"

urlpatterns = [
    path("<int:pk>", room_views.RoomDetailView.as_view(), name="detail"),
    path("search/", room_views.search, name="search"),
]
