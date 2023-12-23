from django.urls import path

from app.views import schema_create_view


urlpatterns = [
    path("schemas/create/", schema_create_view, name="schema_create"),
]
