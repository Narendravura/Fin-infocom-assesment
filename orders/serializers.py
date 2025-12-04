from rest_framework import serializers
from .models import Order, OrderItem, Payment, MenuItem, Category, Menu


class MenuSerializer(serializers.ModelSerializer):
    """Serializer for Menu"""

    class Meta:
        model = Menu
        fields = ['menu_id', 'menu_name']


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for Category"""
    menu_name = serializers.CharField(source='menu.menu_name', read_only=True)

    class Meta:
        model = Category
        fields = ['cat_id', 'category_name', 'menu_name']


class MenuItemSerializer(serializers.ModelSerializer):
    """Serializer for MenuItem"""
    category_name = serializers.CharField(source='category.category_name', read_only=True)
    menu_name = serializers.CharField(source='menu.menu_name', read_only=True)

    class Meta:
        model = MenuItem
        fields = ['item_id', 'item_name', 'category_name', 'menu_name', 'size', 'price']


class OrderItemSerializer(serializers.ModelSerializer):
    """Serializer for OrderItem with full item details"""
    item_name = serializers.CharField(source='item.item_name', read_only=True)
    category_name = serializers.CharField(source='item.category.category_name', read_only=True)

    class Meta:
        model = OrderItem
        fields = [
            'id',
            'item_id',
            'item_name',
            'category_name',
            'size',
            'price',
            'qty',
            'total'
        ]


class PaymentSerializer(serializers.ModelSerializer):
    """Serializer for Payment details"""

    class Meta:
        model = Payment
        fields = [
            'id',
            'payment_id',
            'payment_date',
            'amount_due',
            'tips',
            'discount',
            'total_paid',
            'payment_type',
            'payment_status'
        ]


class OrderDetailSerializer(serializers.ModelSerializer):
    """Complete order serializer with items and payments"""
    items = OrderItemSerializer(many=True, read_only=True)
    payments = PaymentSerializer(many=True, read_only=True)
    total_amount = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    total_paid = serializers.SerializerMethodField()
    payment_balance = serializers.SerializerMethodField()
    item_count = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            'order_id',
            'order_date',
            'order_status',
            'item_count',
            'total_amount',
            'total_paid',
            'payment_balance',
            'items',
            'payments',
            'created_at'
        ]

    def get_total_paid(self, obj):
        """Calculate total amount paid across all payments"""
        return sum(payment.total_paid for payment in obj.payments.all())

    def get_payment_balance(self, obj):
        """Calculate remaining balance"""
        total_paid = self.get_total_paid(obj)
        return obj.total_amount - total_paid

    def get_item_count(self, obj):
        """Count total items in order"""
        return obj.items.count()


class OrderListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for order listing"""
    total_amount = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    total_paid = serializers.SerializerMethodField()
    item_count = serializers.SerializerMethodField()
    payment_count = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            'order_id',
            'order_date',
            'order_status',
            'item_count',
            'payment_count',
            'total_amount',
            'total_paid',
            'created_at'
        ]

    def get_total_paid(self, obj):
        return sum(payment.total_paid for payment in obj.payments.all())

    def get_item_count(self, obj):
        return obj.items.count()

    def get_payment_count(self, obj):
        return obj.payments.count()