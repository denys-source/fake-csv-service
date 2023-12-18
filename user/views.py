from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class LogoutConfirmation(LoginRequiredMixin, TemplateView):
    template_name = "registration/logout_confirmation.html"
