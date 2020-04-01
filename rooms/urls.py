from django.urls import path
from . import views as room_views

app_name = "rooms"

urlpatterns = [
    path("<int:pk>", room_views.room_detail, name="detail"),
]
