from django.shortcuts import redirect, reverse
from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.urls import reverse_lazy


class LoggedOutOnlyView(UserPassesTestMixin):
    def test_func(self):
        return not self.request.user.is_authenticated

    def handle_no_permission(self):
        messages.error(
            self.request,
            "You are already logged in. Please log out to login with different account or to sign up.",
        )
        return redirect("core:home")


class LoggedInOnlyView(LoginRequiredMixin):
    """
    @login_required(login_url=reverse_lazy("users:login"))
    데코레이터를 사용하여 Mixin 을 대체할 수 있다. Perfect Same!
    """

    login_url = reverse_lazy("users:login")


class EmailLoggedInOnlyView(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.login_method == "email"

    def handle_no_permission(self):
        messages.error(
            self.request, f"You were logged in with {self.request.user.login_method}",
        )
        return redirect("core:home")
