from django.views import View
from django.shortcuts import render, redirect, reverse
from . import forms


# Create your views here.
class LoginView(View):
    """ Login View Definition """

    def get(self, request):
        form = forms.LoginForm(initial={"username": "jpark1977@gmail.com"})
        return render(request, "users/login.html", {"form": form})

    def post(self, request):
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
        return render(request, "users/login.html", {"form": form})
