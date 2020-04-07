from django import forms
from . import models


class LoginForm(forms.Form):
    """ Login Form Definition """

    input_username = forms.EmailField()
    input_password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        username = self.cleaned_data.get("input_username")
        password = self.cleaned_data.get("input_password")

        try:
            user = models.User.objects.get(username=username)
            if user.check_password(password):
                return self.cleaned_data
            else:
                self.add_error(
                    "input_password", forms.ValidationError("password is wrong")
                )
        except models.User.DoesNotExist:
            self.add_error(
                "input_username", forms.ValidationError(f"{username} does not exist.")
            )
