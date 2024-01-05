import re

from django.http import HttpRequest

from app.models import Schema


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


def generate_data(schema: Schema, rows: int) -> list[list[str]]:
    columns = schema.columns.all()
    heading = [column.column_name for column in columns]
    res = [heading]
    for _ in range(rows):
        row = [str(column.generate()) for column in columns]
        res.append(row)
    return res
