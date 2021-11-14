from django.contrib import admin

from .models import Customer, Food, FoodCategory, Order, OrderItem, Restaurant


class DeleteNotAllowedModelAdmin(admin.ModelAdmin):

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Customer)
class CustomerAdmin(DeleteNotAllowedModelAdmin):
    pass


@admin.register(Food)
class FoodAdmin(DeleteNotAllowedModelAdmin):
    pass


@admin.register(FoodCategory)
class FoodCategoryAdmin(DeleteNotAllowedModelAdmin):
    pass


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    pass


@admin.register(Restaurant)
class RestaurantAdmin(DeleteNotAllowedModelAdmin):
    list_filter = ['city']
    list_display = ['name', 'city']
