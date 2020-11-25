from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from .models import Csv
# Register your models here.


class CsvAdmin(admin.ModelAdmin):
    list_display = ('__str__',)


admin.site.register(Csv, CsvAdmin)
