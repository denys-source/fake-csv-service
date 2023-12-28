from django.urls import path

from app.views import schema_create_view, schema_update_view


urlpatterns = [
    path("schemas/create/", schema_create_view, name="schema_create"),
    path("schemas/<int:pk>/update/", schema_update_view, name="schema_update"),
]
