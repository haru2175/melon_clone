from http.client import responses

from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth.views import LoginView as DjangoLoginView, RedirectURLMixin
from django.contrib.auth.views import LogoutView as DjangoLogoutView
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from accounts.forms import LoginForm, SignupForm
from accounts.models import User


def is_authenticated(request):
    return JsonResponse({"is_authenticated": request.user.is_authenticated})


class SignupView(RedirectURLMixin, CreateView):
    model = User
    form_class = SignupForm
    template_name = "crispy_form.html"
    extra_context = {
        "form_title": "회원가입",
    }
    success_url = reverse_lazy("accounts:profile")

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            redirect_to = self.success_url
            if redirect_to != request.path:
                messages.warning(request, "로그인 유저는 회원가입을 할 수 없습니다.")
                return HttpResponseRedirect(redirect_to)

        response = super().dispatch(request, *args, **kwargs)
        return response

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "회원가입을 환영합니다 ! ")

        user = self.object
        auth_login(self.request, user)
        messages.success(self.request, "회원가입과 동시에 로그인 지원 ! ")

        # 쿠키 생성
        response.set_cookie("signup_success", "true", max_age=3600)
        return response


signup = SignupView.as_view()


class LoginView(DjangoLoginView):
    redirect_authenticated_user = True
    form_class = LoginForm
    template_name = "crispy_form.html"
    extra_context = {
        "form_title": "로그인",
    }

    def form_valid(self, form):
        # 사용자 인증에 성공하면 메시지를 추가합니다.
        messages.success(self.request, "로그인이 되었습니다.")
        response = super().form_valid(form)

        # 쿠키 생성
        response.set_cookie(
            "login_success", "true", max_age=3600
        )  # 쿠키 유효 기간은 1시간

        return response


login = LoginView.as_view()


class LogoutView(DjangoLogoutView):
    next_page = "accounts:login"

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        messages.success(request, "로그아웃 했습니다.")

        # 쿠키 삭제
        response.delete_cookie("login_success")

        # 로그아웃 시 새로운 쿠키 생성
        response.set_cookie("logout_success", "true", max_age=3600)
        return response


logout = LogoutView.as_view()
