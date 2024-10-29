from django.contrib import admin

from productService.models import Product, Category


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'price']
    search_fields = ['title']
    save_as = True
    fieldsets = [(
        ('Product Info', {
            'fields': ('price', 'title', 'description', 'category')})
    )]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    save_as = True
    fieldsets = [(
        ('Category Info', {
            'fields': ('name', 'description')
        })
    )]
