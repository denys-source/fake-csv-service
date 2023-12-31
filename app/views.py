from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import formset_factory
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.urls import reverse
from django.views.generic import DetailView, FormView, ListView, View
from polymorphic.formsets import (
    polymorphic_inlineformset_factory,
    PolymorphicFormSetChild,
)

from app.forms import FORMS_TO_RENDER, SchemaForm
from app.models import DataType, Schema
from app.utils import get_formsets


class SchemaListView(LoginRequiredMixin, ListView):
    model = Schema
    template_name = "app/schema_list.html"

    def get_queryset(self):
        return Schema.objects.filter(created_by=self.request.user)


@login_required
def schema_create_view(request):
    formset_classes = [formset_factory(form) for _, form in FORMS_TO_RENDER]
    if request.method == "GET":
        schema_form = SchemaForm()
        formsets = get_formsets(formset_classes)
        return render(
            request,
            "app/schema_create.html",
            context={
                "schema_form": schema_form,
                "formsets": formsets,
            },
        )
    elif request.method == "POST":
        schema_form = SchemaForm(request.POST)
        formsets = get_formsets(formset_classes, request)

        if schema_form.is_valid() and all(
            formset.is_valid() for formset in formsets
        ):
            with transaction.atomic():
                schema = schema_form.save(commit=False)
                schema.created_by = request.user
                schema.save()

                for formset in formsets:
                    for form in formset:
                        if form.empty_permitted and not form.has_changed():
                            continue
                        column = form.save(commit=False)
                        column.schema = schema
                        column.save()

            return redirect("schema_list")

        return render(
            request,
            "app/schema_create.html",
            context={"schema_form": schema_form, "formsets": formsets},
        )


@login_required
def schema_update_view(request, pk):
    schema = get_object_or_404(Schema, pk=pk)

    if schema.created_by != request.user:
        return HttpResponseForbidden("You are not allowed to view this page")

    formset_classes = [formset_factory(form) for _, form in FORMS_TO_RENDER]
    formsets = get_formsets(formset_classes)
    child_formsets = [
        PolymorphicFormSetChild(model, form=form)
        for model, form in FORMS_TO_RENDER
    ]
    ColumnInlineFormSet = polymorphic_inlineformset_factory(
        Schema,
        DataType,
        formset_children=child_formsets,
        fields="__all__",
        extra=0,
    )

    if request.method == "GET":
        schema_form = SchemaForm(instance=schema)
        inline_formset = ColumnInlineFormSet(instance=schema)
        return render(
            request,
            "app/schema_update.html",
            context={
                "schema_form": schema_form,
                "inline_formset": inline_formset,
                "formsets": formsets,
            },
        )
    elif request.method == "POST":
        schema_form = SchemaForm(request.POST, instance=schema)
        inline_formset = ColumnInlineFormSet(request.POST, instance=schema)
        formsets = get_formsets(formset_classes, request)

        if (
            schema_form.is_valid()
            and inline_formset.is_valid()
            and all(formset.is_valid() for formset in formsets)
        ):
            with transaction.atomic():
                schema_form.save()
                inline_formset.save()

                for formset in formsets:
                    for form in formset:
                        if form.empty_permitted and not form.has_changed():
                            continue
                        column = form.save(commit=False)
                        column.schema = schema
                        column.save()

            return redirect("schema_list")

        return render(
            request,
            "app/schema_update.html",
            context={
                "schema_form": schema_form,
                "formset": inline_formset,
                "formsets": formsets,
            },
        )
