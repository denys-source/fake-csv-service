from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import formset_factory
from django.http import HttpResponseForbidden
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    DeleteView,
    DetailView,
    FormView,
    ListView,
    View,
)
from django.views.generic.detail import SingleObjectMixin
from polymorphic.formsets import (
    polymorphic_inlineformset_factory,
    PolymorphicFormSetChild,
)

from app.forms import FORMS_TO_RENDER, DataSetForm, SchemaForm
from app.models import DataSetTask, DataType, Schema
from app.tasks import generate_dataset
from app.utils import get_formsets


class UserOwnerMixin:
    def dispatch(self, request, *args, **kwargs):
        if self.get_object().created_by != request.user:
            return HttpResponseForbidden(
                "You are not allowed to view this page"
            )
        return super().dispatch(request, *args, **kwargs)


class SchemaListView(LoginRequiredMixin, ListView):
    model = Schema
    template_name = "app/schema_list.html"

    def get_queryset(self):
        return Schema.objects.filter(created_by=self.request.user)


class SchemaView(View):
    def get(self, request, *args, **kwargs):
        view = SchemaDetailView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = SchemaDataSetFormView.as_view()
        return view(request, *args, **kwargs)


class SchemaDetailView(LoginRequiredMixin, UserOwnerMixin, DetailView):
    model = Schema
    template_name = "app/schema_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = DataSetForm()
        return context


class SchemaDataSetFormView(
    LoginRequiredMixin, UserOwnerMixin, SingleObjectMixin, FormView
):
    model = Schema
    form_class = DataSetForm
    template_name = "app/schema_detail.html"

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()

        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            rows = form.cleaned_data.get("rows")
            task = DataSetTask.objects.create(schema=self.object)
            generate_dataset.delay(self.object.pk, task.pk, rows)
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        success_url = self.get_success_url()
        return HttpResponseRedirect(success_url)

    def get_success_url(self) -> str:
        return reverse("schema_detail", kwargs={"pk": self.object.pk})


class SchemaDeleteView(LoginRequiredMixin, UserOwnerMixin, DeleteView):
    model = Schema
    template_name = "app/schema_delete.html"
    success_url = reverse_lazy("schema_list")

    def form_valid(self, form):
        success_url = self.get_success_url()
        # HACK: django-polymorphic issue #34
        with transaction.atomic():
            columns = DataType.objects.filter(schema=self.object)
            columns.non_polymorphic().delete()
            self.object.delete()
        return HttpResponseRedirect(success_url)


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
        formsets = get_formsets(formset_classes)
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
