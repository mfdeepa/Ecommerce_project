from rest_framework import serializers
from orderServices.models import Order, OrderItem, OrderStatusHistory, OrderTracking


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = [
            'id', 'product_id', 'product_name', 'product_sku',
            'quantity', 'unit_price', 'total_price', 'product_data'
        ]
        read_only_fields = ['id', 'total_price']


class OrderStatusHistorySerializer(serializers.ModelSerializer):
    # created_by_username = serializers.CharField(source='created_by.username', read_only=True)

    class Meta:
        model = OrderStatusHistory
        fields = ['id', 'status', 'notes', 'created_at', 'created_by_id']


class OrderTrackingSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderTracking
        fields = [
            'current_status', 'tracking_events', 'estimated_delivery',
            'actual_delivery', 'created_at', 'updated_at'
        ]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    status_history = OrderStatusHistorySerializer(many=True, read_only=True)
    tracking = OrderTrackingSerializer(read_only=True)
    customer_name = serializers.CharField(source='customer_snapshot.name', read_only=True, default='')

    class Meta:
        model = Order
        fields = [
            'id', 'order_number', 'user_id', 'total_amount',
            'tax_amount', 'shipping_amount', 'discount_amount', 'status',
            'payment_status', 'shipping_address', 'billing_address',
            'created_at', 'updated_at', 'confirmed_at', 'shipped_at',
            'delivered_at', 'notes', 'tracking_number', 'carrier',
            'items', 'status_history', 'tracking', 'customer_name'
        ]
        read_only_fields = ['id', 'order_number', 'created_at', 'updated_at']


class CreateOrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, write_only=True)
    billing_address = serializers.JSONField(required=False)
    user_id = serializers.UUIDField(write_only=True)
    # customer_snapshot = serializers.JSONField(write_only=True)

    class Meta:
        model = Order
        fields = [
            'user_id', 'total_amount', 'tax_amount', 'shipping_amount', 'discount_amount',
            'shipping_address', 'billing_address', 'notes', 'items'
        ]
        extra_kwargs = {
            'user_id': {'required': False, 'allow_null': True}
        }

    def validate_items(self, value):
        if not value:
            raise serializers.ValidationError("At least one item is required.")
        return value

    def create(self, validated_data):
        try:
            items_data = validated_data.pop('items')

            # If billing_address is not provided, use shipping_address as default
            if 'billing_address' not in validated_data or not validated_data['billing_address']:
                validated_data['billing_address'] = validated_data['shipping_address']

            order = Order.objects.create(**validated_data)

            for item_data in items_data:
                OrderItem.objects.create(order=order, **item_data)

            # Create tracking record
            OrderTracking.objects.create(order=order)

            return order
        except Exception as e:
            print(f"Error in CreateOrderSerializer.create: {e}")
            raise serializers.ValidationError(f"Error creating order: {str(e)}")


class OrderSummarySerializer(serializers.ModelSerializer):
    items_count = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            'id', 'order_number', 'total_amount', 'status',
            'created_at', 'items_count'
        ]

    def get_items_count(self, obj):
        return obj.items.count()