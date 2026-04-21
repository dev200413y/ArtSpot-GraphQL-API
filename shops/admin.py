from django.contrib import admin
from .models import Shop


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "address", "created_at")
    search_fields = ("name", "address")
    readonly_fields = ("created_at", "updated_at")
