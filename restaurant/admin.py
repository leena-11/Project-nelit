from django.contrib import admin
from .models import Category, MenuItem, Order, OrderItem

class MenuItemInline(admin.TabularInline):
    model = MenuItem
    extra = 1

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'is_veg')
    list_filter = ('category', 'is_veg')
    search_fields = ('name', 'description')

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('price',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_name', 'phone_number', 'table_number', 'total_amount', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('customer_name', 'phone_number', 'table_number')
    inlines = [OrderItemInline]
    
    # Custom actions to update order status quickly in admin panel
    actions = ['mark_received', 'mark_preparing', 'mark_ready', 'mark_delivered']

    def mark_received(self, request, queryset):
        queryset.update(status='RECEIVED')
    mark_received.short_description = "Mark selected orders as Received"

    def mark_preparing(self, request, queryset):
        queryset.update(status='PREPARING')
    mark_preparing.short_description = "Mark selected orders as Preparing"

    def mark_ready(self, request, queryset):
        queryset.update(status='READY')
    mark_ready.short_description = "Mark selected orders as Ready"

    def mark_delivered(self, request, queryset):
        queryset.update(status='DELIVERED')
    mark_delivered.short_description = "Mark selected orders as Delivered"
