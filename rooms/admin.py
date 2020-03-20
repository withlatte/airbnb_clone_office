from django.contrib import admin
from . import models


# Register your models here.


@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):
    """ Room Admin """

    list_display = (
        "name",
        "country",
        "city",
        "price",
        "guests",
        "beds",
        "bedrooms",
        "baths",
        "check_in",
        "check_out",
        "instant_book",
    )

    list_filter = ("instant_book", "city", "country")

    search_fields = ("=city", "^host__username")


@admin.register(models.RoomType, models.Facility, models.Amenity, models.HouseRule)
class ItemAdmin(admin.ModelAdmin):
    """ Item Admin"""

    pass


@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):
    """ Photo Admin """

    pass
