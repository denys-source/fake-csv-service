from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.views.generic.base import RedirectView
from django.conf.urls.static import static

from user.views import LogoutConfirmation, UserRegisterView

urlpatterns = (
    [
        path("", RedirectView.as_view(pattern_name="schema_list")),
        path("", include("app.urls")),
        path("admin/", admin.site.urls),
        path("accounts/", include("django.contrib.auth.urls")),
        path(
            "accounts/register/", UserRegisterView.as_view(), name="register"
        ),
        path(
            "accounts/confirm-logout/",
            LogoutConfirmation.as_view(),
            name="confirm_logout",
        ),
    ]
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    + (
        [
            path("__debug__/", include("debug_toolbar.urls")),
        ]
        if settings.DEBUG
        else []
    )
)
