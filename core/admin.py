from django.contrib import admin
from .models import Dress, DressImage, Size

class DressImageInline(admin.TabularInline):
    model = DressImage
    extra = 1

@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

@admin.register(Dress)
class DressAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'get_sizes_display', 'created_at']
    search_fields = ['name', 'description', 'price']
    list_filter = ['created_at', 'sizes']
    filter_horizontal = ['sizes']
    inlines = [DressImageInline]
    
    def get_sizes_display(self, obj):
        return ', '.join([size.name for size in obj.sizes.all()]) or "No sizes"
    get_sizes_display.short_description = "Sizes"
