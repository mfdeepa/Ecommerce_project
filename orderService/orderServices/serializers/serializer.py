from rest_framework import serializers

from orderServices.models import OrderItem, OrderTracking, OrderStatusHistory, Order


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product_id', 'title', 'price', 'quantity', 'subtotal']
        read_only_fields = ['subtotal']


class OrderItemCreateSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    title = serializers.CharField(max_length=255)
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    quantity = serializers.IntegerField(min_value=1)


class OrderTrackingSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderTracking
        fields = ['tracking_number', 'carrier', 'estimated_delivery', 'last_updated']


class OrderStatusHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderStatusHistory
        fields = ['status', 'notes', 'created_at', 'created_by_id']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    tracking = OrderTrackingSerializer(read_only=True)
    status_history = OrderStatusHistorySerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'order_number', 'user_id', 'status', 'total_amount',
            'shipping_address', 'billing_address', 'payment_method',
            'customer_snapshot', 'created_at', 'updated_at', 'shipped_at',
            'delivered_at', 'tracking_number', 'carrier', 'items',
            'tracking', 'status_history'
        ]
        read_only_fields = [
            'id', 'order_number', 'created_at', 'updated_at', 'shipped_at',
            'delivered_at', 'items', 'tracking', 'status_history'
        ]


class OrderCreateSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(required=False)  # Will be set from token
    shipping_address = serializers.JSONField()
    billing_address = serializers.JSONField(required=False)
    payment_method = serializers.CharField(max_length=50)
    items = OrderItemCreateSerializer(many=True)

    def validate_items(self, value):
        if not value:
            raise serializers.ValidationError("At least one item is required.")
        return value

    def validate_shipping_address(self, value):
        required_fields = ['street', 'city', 'state', 'zip_code', 'country']
        for field in required_fields:
            if field not in value or not value[field]:
                raise serializers.ValidationError(f"'{field}' is required in shipping address.")
        return value


class OrderUpdateStatusSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=Order.ORDER_STATUS_CHOICES)
    notes = serializers.CharField(required=False, allow_blank=True)
    tracking_data = serializers.DictField(required=False)

    def validate_tracking_data(self, value):
        if value:
            allowed_fields = ['tracking_number', 'carrier', 'estimated_delivery']
            for key in value.keys():
                if key not in allowed_fields:
                    raise serializers.ValidationError(f"'{key}' is not a valid tracking data field.")
        return value