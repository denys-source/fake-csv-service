from django.forms import formset_factory
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from app.forms import (
    DomainNameForm,
    EmailForm,
    FullNameForm,
    IntegerForm,
    JobForm,
    SchemaForm,
)
from app.utils import to_snake_case


FORMS_TO_RENDER = [
    FullNameForm,
    EmailForm,
    JobForm,
    DomainNameForm,
    IntegerForm,
]


@login_required
def schema_create_view(request):
    formset_classes = [formset_factory(form) for form in FORMS_TO_RENDER]
    if request.method == "GET":
        schema_form = SchemaForm()
        formsets = [
            cls(
                prefix=to_snake_case(cls.form._meta.model.__name__),
            )
            for cls in formset_classes
        ]
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
        formsets = [
            cls(
                request.POST,
                prefix=to_snake_case(cls.form._meta.model.__name__),
            )
            for cls in formset_classes
        ]

        if schema_form.is_valid() and all(
            formset.is_valid() for formset in formsets
        ):
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

            return redirect("/")

        return render(
            request,
            "app/schema_create.html",
            context={"schema_form": schema_form, "formsets": formsets},
        )
