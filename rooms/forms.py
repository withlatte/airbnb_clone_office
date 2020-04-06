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
