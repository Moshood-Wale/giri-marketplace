from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Artisan, Product, Order, OrderItem

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'name', 'is_active', 'created_at', 'updated_at')
    search_fields = ('email', 'name')
    ordering = ('-created_at',)
    list_filter = ('is_active', 'is_staff', 'created_at')
    
    # Customize the fields shown in the add/edit forms
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('name',)}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    # Customize the fields shown when creating a new user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'password1', 'password2'),
        }),
    )


@admin.register(Artisan)
class ArtisanAdmin(admin.ModelAdmin):
    list_display = ['business_name', 'location', 'created_at']
    search_fields = ['business_name', 'description', 'location']
    list_filter = ['location', 'created_at']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'artisan', 'price', 'inventory']
    search_fields = ['name', 'description', 'artisan__business_name']
    list_filter = ['artisan', 'created_at']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'status', 'total_amount', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['user__email']  # Changed from user__username to user__email


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'price']
    search_fields = ['order__id', 'product__name']
    list_filter = ['order__status']