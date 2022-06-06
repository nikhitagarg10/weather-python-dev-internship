from django.contrib import admin
from .models.city import City

class AdminCity(admin.ModelAdmin):
    list_display = ["city"]

# Register your models here.
admin.site.register(City, AdminCity)