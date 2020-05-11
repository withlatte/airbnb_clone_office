from django import forms
from django_countries.fields import CountryField
from . import models


class SearchForm(forms.Form):
    """ Search Form Definition """

    city = forms.CharField(initial="Anywhere")
    country = CountryField(default="KR").formfield()
    room_type = forms.ModelChoiceField(
        required=False, empty_label="Any Kind", queryset=models.RoomType.objects.all()
    )
    price = forms.IntegerField(required=False)
    guests = forms.IntegerField(
        required=False, help_text="How many guests do you want to be stayed?"
    )
    beds = forms.IntegerField(required=False)
    bedrooms = forms.IntegerField(required=False)
    baths = forms.IntegerField(required=False)
    instant_book = forms.BooleanField(required=False)
    super_host = forms.BooleanField(required=False)

    amenities = forms.ModelMultipleChoiceField(
        models.Amenity.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        help_text="Select as many as you want.",
    )
    facilities = forms.ModelMultipleChoiceField(
        models.Facility.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        help_text="Select as many as you want.",
    )


class CreatePhotoForm(forms.ModelForm):
    """ Create Photo Form """

    class Meta:
        model = models.Photo
        fields = (
            "caption",
            "file",
        )

    def save(self, pk, *args, **kwargs):
        photo = super().save(commit=False)
        room = models.Room.objects.get(pk=pk)
        photo.room = room
        photo.save()


class CreateRoomForm(forms.ModelForm):
    """ Create Room Form Definition """

    class Meta:
        model = models.Room
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

    def save(self, *args, **kwargs):
        room = super().save(commit=False)
        return room
