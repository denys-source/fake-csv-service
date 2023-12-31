from django.urls import path

from app.views import (
    SchemaDeleteView,
    SchemaView,
    schema_create_view,
    schema_update_view,
    SchemaListView,
)


urlpatterns = [
    path("schemas/", SchemaListView.as_view(), name="schema_list"),
    path("schemas/<int:pk>/", SchemaView.as_view(), name="schema_detail"),
    path("schemas/create/", schema_create_view, name="schema_create"),
    path("schemas/<int:pk>/update/", schema_update_view, name="schema_update"),
    path(
        "schemas/<int:pk>/delete/",
        SchemaDeleteView.as_view(),
        name="schema_delete",
    ),
]
