from django.contrib import admin

from app.models import DataType, Schema


admin.site.register(Schema)
admin.site.register(DataType)
