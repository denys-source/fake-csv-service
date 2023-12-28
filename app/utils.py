import re

from django.http import HttpRequest


def to_snake_case(s: str) -> str:
    return re.sub(r"(?<!^)(?=[A-Z])", "_", s).lower()


def get_formsets(
    formset_classes: list,
    request: HttpRequest | None = None,
) -> list:
    if request:
        return [
            cls(
                request.POST,
                prefix=to_snake_case(cls.form._meta.model.__name__),
            )
            for cls in formset_classes
        ]
    return [
        cls(
            prefix=to_snake_case(cls.form._meta.model.__name__),
        )
        for cls in formset_classes
    ]
