from django.contrib import admin
from .models import Order, OrderItems


class OrderItemsInline(admin.TabularInline):
    model = OrderItems
    extra = 0
    readonly_fields = ["product", "quantity"]
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "buyer",
        "get_total_items",
        "get_total_amount",
        "created_at",
        "updated_at",
    ]
    list_filter = ["created_at", "updated_at"]
    search_fields = ["buyer__username", "buyer__email", "id"]
    ordering = ["-created_at"]
    readonly_fields = ["created_at", "updated_at", "buyer"]

    inlines = [OrderItemsInline]

    fieldsets = (
        ("Order Information", {"fields": ("buyer",)}),
        (
            "Timestamps",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )

    list_per_page = 25

    def get_total_items(self, obj):
        return obj.orderitems_set.count()

    get_total_items.short_description = "Total Items"

    def get_total_amount(self, obj):
        total = sum(
            item.product.price * item.quantity for item in obj.orderitems_set.all()
        )
        return f"${total:.2f}"

    get_total_amount.short_description = "Total Amount"

    def has_add_permission(self, request):
        # Prevent adding orders through admin (should be created via API)
        return False


@admin.register(OrderItems)
class OrderItemsAdmin(admin.ModelAdmin):
    list_display = ["id", "order", "product", "quantity", "get_item_total"]
    list_filter = ["order__created_at", "product__Category"]
    search_fields = ["order__id", "product__name", "order__buyer__username"]
    ordering = ["-order__created_at"]
    readonly_fields = ["order", "product", "quantity"]

    def get_item_total(self, obj):
        return f"${obj.product.price * obj.quantity:.2f}"

    get_item_total.short_description = "Item Total"

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
