from django.contrib import admin
from .models import Menu, Category, MenuItem, Order, OrderItem, Payment


class OrderItemInline(admin.TabularInline):
    """Inline display of order items within order admin"""
    model = OrderItem
    extra = 0
    fields = ('item', 'size', 'price', 'qty', 'total')
    readonly_fields = ('total',)


class PaymentInline(admin.TabularInline):
    """Inline display of payments within order admin"""
    model = Payment
    extra = 0
    fields = ('payment_id', 'payment_date', 'amount_due', 'total_paid',
              'payment_type', 'payment_status', 'tips', 'discount')


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    """Admin configuration for Menu"""
    list_display = ('menu_id', 'menu_name')
    search_fields = ('menu_name',)
    ordering = ('menu_id',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin configuration for Category"""
    list_display = ('cat_id', 'category_name', 'menu')
    list_filter = ('menu',)
    search_fields = ('category_name',)
    ordering = ('cat_id',)


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    """Admin configuration for MenuItem"""
    list_display = ('item_id', 'item_name', 'category', 'menu', 'size', 'price')
    list_filter = ('category', 'menu')
    search_fields = ('item_name',)
    ordering = ('item_id',)

    fieldsets = (
        ('Basic Information', {
            'fields': ('item_id', 'item_name', 'category', 'menu')
        }),
        ('Pricing', {
            'fields': ('size', 'price'),
            'description': 'Use comma-separated values for multiple sizes/prices'
        }),
    )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Admin configuration for Order"""
    list_display = ('order_id', 'order_date', 'order_status', 'get_total_amount',
                    'get_item_count', 'get_payment_count')
    list_filter = ('order_status', 'order_date')
    search_fields = ('order_id',)
    date_hierarchy = 'order_date'
    ordering = ('-order_date', '-order_id')
    inlines = [OrderItemInline, PaymentInline]

    readonly_fields = ('get_total_amount', 'created_at')

    fieldsets = (
        ('Order Information', {
            'fields': ('order_id', 'order_date', 'order_status')
        }),
        ('Summary', {
            'fields': ('get_total_amount', 'created_at'),
            'classes': ('collapse',)
        }),
    )

    def get_total_amount(self, obj):
        """Display total order amount"""
        return f"${obj.total_amount:.2f}"

    get_total_amount.short_description = 'Total Amount'

    def get_item_count(self, obj):
        """Display number of items"""
        return obj.items.count()

    get_item_count.short_description = 'Items'

    def get_payment_count(self, obj):
        """Display number of payments"""
        return obj.payments.count()

    get_payment_count.short_description = 'Payments'


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    """Admin configuration for OrderItem"""
    list_display = ('id', 'order', 'item', 'size', 'price', 'qty', 'total')
    list_filter = ('order__order_date', 'item__category')
    search_fields = ('order__order_id', 'item__item_name')
    ordering = ('-order__order_date', 'order__order_id')

    readonly_fields = ('total',)

    fieldsets = (
        ('Order Information', {
            'fields': ('order',)
        }),
        ('Item Details', {
            'fields': ('item', 'size', 'price', 'qty')
        }),
        ('Calculated Fields', {
            'fields': ('total',),
            'classes': ('collapse',)
        }),
    )


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    """Admin configuration for Payment"""
    list_display = ('payment_id', 'order', 'payment_date', 'total_paid',
                    'payment_type', 'payment_status', 'amount_due')
    list_filter = ('payment_status', 'payment_type', 'payment_date')
    search_fields = ('payment_id', 'order__order_id')
    date_hierarchy = 'payment_date'
    ordering = ('-payment_date', '-payment_id')

    readonly_fields = ('created_at',)

    fieldsets = (
        ('Payment Information', {
            'fields': ('payment_id', 'order', 'payment_date')
        }),
        ('Amount Details', {
            'fields': ('amount_due', 'total_paid', 'tips', 'discount')
        }),
        ('Payment Status', {
            'fields': ('payment_type', 'payment_status')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

    def get_queryset(self, request):
        """Optimize queryset with related objects"""
        qs = super().get_queryset(request)
        return qs.select_related('order')


# Customize admin site header and title
admin.site.site_header = "Restaurant Order Management System"
admin.site.site_title = "Restaurant Admin"
admin.site.index_title = "Welcome to Restaurant Order Management"