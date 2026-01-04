from django.contrib import admin
from .models import Dress, DressImage, Size, MenProduct, HandmadeItem

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

@admin.register(MenProduct)
class MenProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'get_image_count', 'get_sizes_display', 'created_at']
    search_fields = ['name', 'description']
    list_filter = ['created_at']
    filter_horizontal = ['sizes']
    
    def get_image_count(self, obj):
        return len(obj.image_urls)  # ✅ @property works!
    get_image_count.short_description = "Images"
    
    def get_sizes_display(self, obj):
        return ', '.join([size.name for size in obj.sizes.all()]) or "No sizes"
    get_sizes_display.short_description = "Sizes"
    
    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'image_urls_text':
            kwargs['widget'] = admin.widgets.AdminTextareaWidget(attrs={'rows': 5})
            kwargs['help_text'] = 'Paste URLs ONE PER LINE'
        return super().formfield_for_dbfield(db_field, **kwargs)

@admin.register(HandmadeItem)
class HandmadeItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'get_image_count', 'get_sizes_display', 'created_at']
    search_fields = ['name', 'description']
    list_filter = ['created_at']
    filter_horizontal = ['sizes']
    
    def get_image_count(self, obj):
        return len(obj.image_urls)
    get_image_count.short_description = "Images"
    
    def get_sizes_display(self, obj):
        return ', '.join([size.name for size in obj.sizes.all()]) or "No sizes"
    get_sizes_display.short_description = "Sizes"
    
    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'image_urls_text':
            kwargs['widget'] = admin.widgets.AdminTextareaWidget(attrs={'rows': 5})
            kwargs['help_text'] = 'Paste URLs ONE PER LINE'
        return super().formfield_for_dbfield(db_field, **kwargs)

@admin.register(DressImage)
class DressImageAdmin(admin.ModelAdmin):
    list_display = ['dress', 'image']
    list_filter = ['dress']
