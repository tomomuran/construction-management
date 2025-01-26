from django.contrib import admin
from .models import MaterialCategory, Material, MaterialTransaction


@admin.register(MaterialCategory)
class MaterialCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name", "description")


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = (
        "code",
        "name",
        "category",
        "specification",
        "unit",
        "unit_price",
        "current_stock",
        "minimum_stock",
    )
    list_filter = ("category", "unit")
    search_fields = ("code", "name", "specification")
    ordering = ("category", "code")


@admin.register(MaterialTransaction)
class MaterialTransactionAdmin(admin.ModelAdmin):
    list_display = (
        "transaction_date",
        "material",
        "transaction_type",
        "quantity",
        "unit_price",
        "project",
        "order_number",
    )
    list_filter = ("transaction_type", "material__category", "project")
    search_fields = ("material__name", "order_number", "delivery_number")
    date_hierarchy = "transaction_date"
