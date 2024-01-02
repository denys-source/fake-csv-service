from django.contrib import admin

from app.models import DataSetTask, DataType, Schema


admin.site.register(Schema)
admin.site.register(DataType)
admin.site.register(DataSetTask)
