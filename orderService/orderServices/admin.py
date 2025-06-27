# from django.contrib import admin
# from .models import Order, OrderItem, OrderStatusHistory, OrderTracking
#
#
# class OrderItemInline(admin.TabularInline):
#     model = OrderItem
#     extra = 0
#     readonly_fields = ('total_price',)
#
#
# class OrderStatusHistoryInline(admin.TabularInline):
#     model = OrderStatusHistory
#     extra = 0
#     readonly_fields = ('created_at',)
#
#
# @admin.register(Order)
# class OrderAdmin(admin.ModelAdmin):
#     list_display = [
#         'order_number', 'user', 'status', 'payment_status',
#         'total_amount', 'created_at'
#     ]
#     list_filter = ['status', 'payment_status', 'created_at']
#     search_fields = ['order_number', 'user__username', 'user__email']
#     readonly_fields = ['id', 'order_number', 'created_at', 'updated_at']
#     inlines = [OrderItemInline, OrderStatusHistoryInline]
#
#     fieldsets = (
#         ('Order Information', {
#             'fields': ('id', 'order_number', 'user', 'status', 'payment_status')
#         }),
#         ('Amounts', {
#             'fields': ('total_amount', 'tax_amount', 'shipping_amount', 'discount_amount')
#         }),
#         ('Addresses', {
#             'fields': ('shipping_address', 'billing_address')
#         }),
#         ('Shipping Information', {
#             'fields': ('tracking_number', 'carrier')
#         }),
#         ('Timestamps', {
#             'fields': ('created_at', 'updated_at', 'confirmed_at', 'shipped_at', 'delivered_at')
#         }),
#         ('Additional Information', {
#             'fields': ('notes',)
#         }),
#     )
#
#
# @admin.register(OrderTracking)
# class OrderTrackingAdmin(admin.ModelAdmin):
#     list_display = ['order', 'current_status', 'estimated_delivery', 'updated_at']
#     list_filter = ['current_status']
#     search_fields = ['order__order_number']