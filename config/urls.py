from django.contrib import admin
from django.urls import include, path

from user.views import LogoutConfirmation

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path(
        "accounts/confirm-logout/",
        LogoutConfirmation.as_view(),
        name="confirm_logout",
    ),
]
