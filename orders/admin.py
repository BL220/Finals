from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'quantity', 'price', 'subtotal')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'full_name', 'status', 'created_at', 'total_price', 'delete_action')
    list_filter = ('status', 'created_at')
    list_editable = ('status',)
    search_fields = ('full_name', 'phone')
    inlines = [OrderItemInline]
    actions = None

    def delete_action(self, obj):
        url = reverse('admin:orders_order_delete', args=[obj.pk])
        return format_html('<a href="{}" class="deletelink">Delete</a>', url)
    delete_action.short_description = 'Delete'

    class Media:
        css = {'all': ('css/admin_custom.css',)}
