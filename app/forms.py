from django import forms

from app.models import (
    DomainName,
    Email,
    FullName,
    Integer,
    Job,
    Schema,
)


FORMS_TO_RENDER = []


def render_in_formset(cls):
    FORMS_TO_RENDER.append((cls._meta.model, cls))
    return cls


class SchemaForm(forms.ModelForm):
    class Meta:
        model = Schema
        fields = ("name", "delimiter", "quotechar")
        labels = {
            "delimiter": "Column separator",
            "quotechar": "String character",
        }


@render_in_formset
class FullNameForm(forms.ModelForm):
    class Meta:
        model = FullName
        fields = ("column_name", "order")


@render_in_formset
class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ("column_name", "order")


@render_in_formset
class EmailForm(forms.ModelForm):
    class Meta:
        model = Email
        fields = ("column_name", "order")


@render_in_formset
class DomainNameForm(forms.ModelForm):
    class Meta:
        model = DomainName
        fields = ("column_name", "order")


@render_in_formset
class IntegerForm(forms.ModelForm):
    class Meta:
        model = Integer
        fields = ("column_name", "order", "from_bound", "to_bound")
        labels = {"from_bound": "From", "to_bound": "To"}
