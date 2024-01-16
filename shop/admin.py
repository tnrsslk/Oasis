from django.contrib import admin
from .models import Category, Product, Variation, ReviewRating, ProductGallery
import admin_thumbnails

# Используем декоратор admin_thumbnails.thumbnail для отображения миниатюр изображений в админ-панели
@admin_thumbnails.thumbnail('image')
class ProductGalleryInline(admin.TabularInline):
    model = ProductGallery
    extra = 1

# Регистрируем модель Category в админ-панели
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

# Регистрируем модель Product в админ-панели
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'new', 'discount', 'stock', 'created', 'updated', 'is_available']
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ['is_available', 'category', 'new']
    list_editable = ['price', 'discount', 'is_available', 'stock', 'new']
    readonly_fields = ['created', 'updated', ]
    inlines = [ProductGalleryInline]  # Встраиваем ProductGalleryInline в админ-панель продукта

# Регистрируем модель Variation в админ-панели
@admin.register(Variation)
class VariationAdmin(admin.ModelAdmin):
    list_display = ['product', 'variation_category', 'variation_value', 'is_active']
    list_filter = ['product', 'variation_category', 'is_active']
    list_editable = ['is_active']


# Регистрируем модель ReviewRating в админ-панели
@admin.register(ReviewRating)
class ReviewRatingAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'update_at', 'status')
    readonly_fields = ('product', 'user', 'review', 'rating', 'ip', 'status', 'created_at', 'updated_at')

    def has_add_permission(self, request):
        return False  # Запретить добавление новых отзывов через админ-панель

    def has_change_permission(self, request, obj=None):
        return False  # Запретить редактирование существующих отзывов

    def has_delete_permission(self, request, obj=None):
        return False  # Запретить удаление существующих отзывов


# Регистрируем модель ProductGallery в админ-панели
@admin.register(ProductGallery)
class ProductGalleryAdmin(admin.ModelAdmin):
    list_filter = ['product']

