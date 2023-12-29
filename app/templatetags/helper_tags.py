from django import template


register = template.Library()


@register.simple_tag
def get_formset_name(formset):
    return formset.form._meta.model._meta.verbose_name

@register.simple_tag
def get_form_name(form):
    return form._meta.model._meta.verbose_name

@register.simple_tag
def get_column_type(column):
    return column._meta.verbose_name
