from django.contrib import admin
from .models import Product
from .models import ContactMessage

admin.site.register(ContactMessage)
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price', 'is_latest', 'is_offer']  # ✅ Added is_latest
    search_fields = ['name']
    list_filter = ['price', 'is_latest', 'is_offer']  # ✅ Optional: filter by is_latest
    list_editable = ['is_latest', 'is_offer']  # ✅ Make it editable directly in list view

