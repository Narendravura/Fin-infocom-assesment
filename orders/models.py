from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal


class Menu(models.Model):
    """Restaurant menu (Food/Drinks)"""
    menu_id = models.IntegerField(primary_key=True)
    menu_name = models.CharField(max_length=100)

    class Meta:
        db_table = 'menu'
        ordering = ['menu_id']

    def __str__(self):
        return self.menu_name


class Category(models.Model):
    """Menu categories (Starters, Mains, etc.)"""
    cat_id = models.IntegerField(primary_key=True)
    category_name = models.CharField(max_length=100)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, db_column='menu_id')

    class Meta:
        db_table = 'category'
        ordering = ['cat_id']

    def __str__(self):
        return self.category_name


class MenuItem(models.Model):
    """Individual menu items"""
    item_id = models.IntegerField(primary_key=True)
    item_name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, db_column='cat_id')
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, db_column='menu_id')
    size = models.CharField(max_length=50, blank=True, null=True,
                            help_text="Comma-separated sizes if applicable")
    price = models.CharField(max_length=50,
                             help_text="Comma-separated prices matching sizes")

    class Meta:
        db_table = 'menu_item'
        ordering = ['item_id']

    def __str__(self):
        return self.item_name

    def get_price_for_size(self, size=None):
        """Get price for specific size or default price"""
        prices = [Decimal(p.strip()) for p in self.price.split(',')]

        if not size or not self.size:
            return prices[0]

        sizes = [s.strip() for s in self.size.split(',')]
        try:
            index = sizes.index(size)
            return prices[index]
        except (ValueError, IndexError):
            return prices[0]


class Order(models.Model):
    """Master order table"""
    order_id = models.IntegerField(primary_key=True)
    order_date = models.DateField()
    order_status = models.CharField(max_length=50, default='Completed')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'orders'
        ordering = ['-order_date', '-order_id']

    def __str__(self):
        return f"Order #{self.order_id}"

    @property
    def total_amount(self):
        """Calculate total from order items"""
        return sum(item.total for item in self.items.all())


class OrderItem(models.Model):
    """Individual items in an order"""
    id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE,
                              related_name='items', db_column='order_id')
    item = models.ForeignKey(MenuItem, on_delete=models.CASCADE, db_column='item_id')
    size = models.CharField(max_length=20, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=5,
                                validators=[MinValueValidator(Decimal('0.01'))])
    qty = models.IntegerField(validators=[MinValueValidator(1)])
    total = models.DecimalField(max_digits=10, decimal_places=5)

    class Meta:
        db_table = 'order_items'
        indexes = [
            models.Index(fields=['order']),
        ]

    def __str__(self):
        return f"{self.item.item_name} x{self.qty}"

    def save(self, *args, **kwargs):
        """Auto-calculate total before saving"""
        self.total = self.price * self.qty
        super().save(*args, **kwargs)


class Payment(models.Model):
    """Payment transactions"""
    PAYMENT_TYPE_CHOICES = [
        ('Card', 'Card'),
        ('Cash', 'Cash'),
        ('UPI', 'UPI'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('Completed', 'Completed'),
        ('Pending', 'Pending'),
        ('Refunded', 'Refunded'),
        ('Failed', 'Failed'),
    ]

    id = models.AutoField(primary_key=True)
    payment_id = models.IntegerField(unique=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE,
                              related_name='payments', db_column='order_id')
    payment_date = models.DateField()
    amount_due = models.DecimalField(max_digits=10, decimal_places=5)
    tips = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPE_CHOICES)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'payments'
        ordering = ['-payment_date', '-payment_id']
        indexes = [
            models.Index(fields=['order']),
            models.Index(fields=['payment_status']),
        ]

    def __str__(self):
        return f"Payment #{self.payment_id} - {self.payment_type}"



