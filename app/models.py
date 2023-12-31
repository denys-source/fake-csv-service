import random
from typing import Any

from faker import Faker
from django.db import models
from django.core.exceptions import ValidationError
from django.conf import settings
from polymorphic.models import PolymorphicModel


fake = Faker()


class Schema(models.Model):
    DELIMITERS = [
        (",", "Comma (,)"),
        (";", "Semicolon (;)"),
        ("|", "Bar (|)"),
        ("\t", "Tab"),
        (" ", "Space"),
    ]
    QUOTECHARS = [
        ('"', 'Double-quote (")'),
        ("'", "Single-quote (')"),
    ]
    name = models.CharField(max_length=63)
    delimiter = models.CharField(max_length=1, choices=DELIMITERS)
    quotechar = models.CharField(max_length=1, choices=QUOTECHARS)
    modified = models.DateField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="schemas",
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ("name",)

    def __str__(self) -> str:
        return self.name


class DataSetTask(models.Model):
    STATUSES = [
        ("processing", "Processing"),
        ("failed", "Failed"),
        ("ready", "Ready"),
    ]
    status = models.CharField(
        max_length=63, choices=STATUSES, default="processing"
    )
    created = models.DateField(auto_now_add=True)
    file = models.FileField(upload_to="uploads/%Y/%m/%d/", null=True)
    schema = models.ForeignKey(
        Schema, related_name="datasets", on_delete=models.CASCADE
    )

    def __str__(self) -> str:
        return f"Data set for {self.schema.name}: {self.status}"


class DataType(PolymorphicModel):
    column_name = models.CharField(max_length=63)
    order = models.PositiveIntegerField()
    schema = models.ForeignKey(
        Schema, related_name="columns", on_delete=models.CASCADE
    )

    class Meta:
        ordering = ("order",)

    def __str__(self) -> str:
        return self.column_name


class FullName(DataType):
    class Meta(DataType.Meta):
        verbose_name = "Full Name"

    def generate(self) -> Any:
        return fake.name()


class Job(DataType):
    class Meta(DataType.Meta):
        verbose_name = "Job"

    def generate(self) -> Any:
        return fake.job()


class Email(DataType):
    class Meta(DataType.Meta):
        verbose_name = "Email"

    def generate(self) -> Any:
        return fake.email()


class DomainName(DataType):
    class Meta(DataType.Meta):
        verbose_name = "Domain Name"

    def generate(self) -> Any:
        return fake.domain_name()


class Integer(DataType):
    from_bound = models.IntegerField()
    to_bound = models.IntegerField()

    class Meta(DataType.Meta):
        verbose_name = "Integer"

    def clean(self) -> None:
        if self.from_bound and self.to_bound:
            if self.from_bound > self.to_bound:
                raise ValidationError("From must be <= to")

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def generate(self) -> Any:
        return random.randint(self.from_bound, self.to_bound)
