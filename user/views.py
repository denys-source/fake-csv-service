from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from user.forms import RegisterForm


class LogoutConfirmation(LoginRequiredMixin, TemplateView):
    template_name = "registration/logout_confirmation.html"


class UserRegisterView(CreateView):
    model = get_user_model()
    form_class = RegisterForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("login")
