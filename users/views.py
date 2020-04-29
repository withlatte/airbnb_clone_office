import os
import requests
from django.views.generic import FormView, DetailView, UpdateView
from django.urls import reverse_lazy
from django.shortcuts import redirect, reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.files.base import ContentFile
from django.contrib import messages
from . import forms, models, mixins


class LoginView(mixins.LoggedOutOnlyView, FormView):
    template_name = "users/login.html"
    form_class = forms.LoginForm

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            messages.success(self.request, f"Welcome back {user.first_name}")
            login(self.request, user)
        return super().form_valid(form)

    def get_success_url(self):
        get_next_url = self.request.GET.get("next")
        if get_next_url is not None:
            return get_next_url
        else:
            return reverse("core:home")


def log_out(request):
    messages.info(request, f"Good Bye! {request.user.first_name}")
    logout(request)
    return redirect(reverse("users:login"))


class SignUpView(mixins.LoggedOutOnlyView, FormView):
    template_name = "users/signup.html"
    form_class = forms.SignUpForm
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):
        form.save()
        email = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password2")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            messages.success(self.request, f"Welcome {user.first_name}")
            login(self.request, user)
        if user.email == "":
            user.email = email
        user.verify_email()
        return super().form_valid(form)


def complete_verification(request, key):
    try:
        user = models.User.objects.get(email_secret=key)
        user.email_confirmed = True
        user.email_secret = ""
        user.save()
        # todo add success message
    except models.User.DoesNotExist:
        # todo add error message
        pass
    return redirect(reverse("core:home"))


class GithubException(Exception):
    pass


def github_login(request):
    client_id = os.environ.get("GH_USERNAME")
    redirect_uri = "http://127.0.0.1:8000/users/login/github/callback"
    return redirect(
        f"https://github.com/login/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&scope=read:user"
    )


def github_callback(request):
    try:
        code = request.GET.get("code", None)
        client_id = os.environ.get("GH_USERNAME")
        client_secret = os.environ.get("GH_SECRET")
        if code is not None:
            result = requests.post(
                f"https://github.com/login/oauth/access_token?client_id={client_id}&client_secret={client_secret}&code={code}",
                headers={"Accept": "application/json"},
            )
            result_json = result.json()
            error = result_json.get("error", None)
            if error is not None:
                return redirect(reverse("users:login"))
            else:
                access_token = result_json.get("access_token")
                profile_request = requests.get(
                    "https://api.github.com/user",
                    headers={
                        "Authorization": f"token {access_token}",
                        "Accept": "application/json",
                    },
                )
                profile_json = profile_request.json()
                username = profile_json.get("login", None)
                if username is not None:
                    name = username
                    email = profile_json.get("email")
                    bio = profile_json.get("bio")
                    try:
                        user = models.User.objects.get(email=email)
                        if user.login_method != models.User.LOGIN_GITHUB:
                            raise GithubException(
                                f"Please log in with: {user.login_method}"
                            )
                    except models.User.DoesNotExist:
                        user = models.User.objects.create(
                            username=email,
                            email=email,
                            first_name=name,
                            bio=bio,
                            login_method=models.User.LOGIN_GITHUB,
                        )
                        user.set_unusable_password()
                        user.save()
                    messages.success(request, f"Welcome back {user.first_name}")
                    login(request, user)
                    return redirect(reverse("core:home"))
                else:
                    raise GithubException("Can't get your profile")
        else:
            raise GithubException("Can't get the authorization code")
    except GithubException as e:
        messages.error(request, e)
        return redirect(reverse("users:login"))


def kakao_login(request):
    client_id = os.environ.get("KAKAO_ID")
    redirect_uri = "http://127.0.0.1:8000/users/login/kakao/callback"

    return redirect(
        f"https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code"
    )


class KakaoException(Exception):
    pass


def kakao_callback(request):
    try:
        client_id = os.environ.get("KAKAO_ID")
        client_secret = os.environ.get("KAKAO_KEY")
        redirect_uri = "http://127.0.0.1:8000/users/login/kakao/callback"
        code = request.GET.get("code", None)
        if code is not None:
            token_request = requests.post(
                f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={client_id}&client_secret={client_secret}&code={code}&redirect_uri={redirect_uri}",
            )
            token_json = token_request.json()
            error = token_json.get("error", None)
            if error is not None:
                raise KakaoException("Can't get the access token")
            else:
                access_token = token_json.get("access_token")
                profile_request = requests.get(
                    "https://kapi.kakao.com/v2/user/me",
                    headers={"Authorization": f"Bearer {access_token}",},
                )
                profile_json = profile_request.json()
                kakao_account = profile_json.get("kakao_account")
                properties = profile_json.get("properties")
                profile = kakao_account.get("profile")
                email = kakao_account.get("email", None)
                if email is not None:
                    name = profile.get("nickname")
                    gender = kakao_account.get("gender")
                    profile_image = properties.get("profile_image")
                    try:
                        user = models.User.objects.get(email=email)
                        if user.login_method != models.User.LOGIN_KAKAO:
                            raise KakaoException(
                                f"Please log in with: {user.login_method}"
                            )
                    except models.User.DoesNotExist:
                        user = models.User.objects.create(
                            username=email,
                            first_name=name,
                            email=email,
                            gender=gender,
                            login_method=models.User.LOGIN_KAKAO,
                            email_confirmed=True,
                        )
                        user.set_unusable_password()
                        user.save()
                        if profile_image is not None:
                            photo_request = requests.get(profile_image)
                            user.avatar.save(
                                f"{email}-avatar", ContentFile(photo_request.content)
                            )
                    messages.success(request, f"Welcome back {user.first_name}")
                    login(request, user)
                    return redirect(reverse("core:home"))
                else:
                    raise KakaoException("Can't get your profile")
        else:
            raise KakaoException("Can't get the authorization code")
    except KakaoException as e:
        messages.error(request, e)
        return redirect(reverse("users:login"))


class UserProfileView(DetailView):
    """
    User Profile View Definition
    Nomadcoder Lesson #21.3 참조
    페이지 이동에 따라 유저가 변경되는 구조에 따라
    context_obj_name 을 설정하여 어느 페이지에서든
    오른쪽 상단의 PROFILE 버튼을 클릭 시
    '로그인한 유저'에 대한 프로파일 페이지로 이동하게 한다.
    """

    model = models.User
    context_object_name = "user_obj"

    def get_context_data(self, *, object_list=None, **kwargs):
        """
        super().get_context_data(**kwargs) 이 구문은 위 context_object_name 을
        불러온다(기본값). 추가 인자를 불러오고 싶을 때, get_context_data 를
        오버라이드 하여 추가할 수 있다. 아래의 Hello 문 처럼 배열에 추가한다.
        """
        context = super().get_context_data(**kwargs)
        context["hello"] = "Hello!"
        # html 파일에서 {{hello}} 로 불러 사용한다.
        return context


class UpdateProfileView(mixins.LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    Update Profile View Definition :
    UpdateView 클래스뷰 사용 시, urls.py 에 path 입력 시, <int:pk> 와 같은
    형식으로 url 을 부여하면 자동으로 모든 update 프로세스를 만들어 준다.
    그러나, 지금처럼 update-profile 형식의 path 설정 시, get_object() 를
    오버라이드 하여, 내가 원하는 스타일로 커스터마이징 할 수 있다.
    """

    model = models.User
    form_class = forms.UpdateProfileForm
    template_name = "users/update-profile.html"
    success_message = "Profile updated successfully"

    def get_object(self, queryset=None):
        return self.request.user

    """
    form_valid function 을 사용하여 클래스뷰의 객체에 접근하여
    각 인스턴스를 핸들링 할 수 있다. 아래는 이메일 변경 시, 자동으로
    유저네임까지 같은 이메일로 변경 해 주는 프로세스이다.
    
    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        self.object.username = email
        self.object.save()
        return super(UpdateProfileView, self).form_valid(form)
    """


class UpdatePasswordView(
    mixins.EmailLoggedInOnlyView,
    mixins.LoginRequiredMixin,
    SuccessMessageMixin,
    PasswordChangeView,
):
    """ Update Password View Definition """

    template_name = "users/update-password.html"
    success_message = "Password updated successfully"

    def get_form(self, form_class=None):
        form = super(UpdatePasswordView, self).get_form(form_class=form_class)

        form.fields["old_password"].widget.attrs = {"placeholder": "Current Password"}
        form.fields["new_password1"].widget.attrs = {"placeholder": "New Password"}
        form.fields["new_password2"].widget.attrs = {
            "placeholder": "New Password Confirmation"
        }
        return form

    def get_success_url(self):
        return reverse("users:profile", kwargs={"pk": self.request.user.pk})
