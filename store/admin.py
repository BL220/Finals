from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User, Group
from django.utils.html import format_html
from django.urls import reverse
from .models import Category, Product, CartItem

admin.site.site_header = 'Tech Store Admin'
admin.site.site_title = 'Tech Store'

admin.site.unregister(User)
admin.site.unregister(Group)


def delete_button(obj, app_label, model_name):
    url = reverse(f'admin:{app_label}_{model_name}_delete', args=[obj.pk])
    return format_html('<a href="{}" class="deletelink">Delete</a>', url)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'is_staff', 'delete_action')
    list_filter = ('is_staff', 'is_superuser')
    actions = None
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
    )

    def delete_action(self, obj):
        return delete_button(obj, 'auth', 'user')
    delete_action.short_description = 'Delete'

    class Media:
        css = {'all': ('css/admin_custom.css',)}


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'delete_action')
    prepopulated_fields = {'slug': ('name',)}
    actions = None

    def delete_action(self, obj):
        return delete_button(obj, 'store', 'category')
    delete_action.short_description = 'Delete'

    class Media:
        css = {'all': ('css/admin_custom.css',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock', 'is_available', 'created_at', 'delete_action')
    list_filter = ('category', 'is_available')
    list_editable = ('price', 'stock', 'is_available')
    search_fields = ('name', 'description')
    actions = None

    def delete_action(self, obj):
        return delete_button(obj, 'store', 'product')
    delete_action.short_description = 'Delete'

    class Media:
        css = {'all': ('css/admin_custom.css',)}


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'delete_action')
    list_filter = ('user',)
    actions = None

    def delete_action(self, obj):
        return delete_button(obj, 'store', 'cartitem')
    delete_action.short_description = 'Delete'

    class Media:
        css = {'all': ('css/admin_custom.css',)}
