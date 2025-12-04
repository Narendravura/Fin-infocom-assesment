"""
Django management command to import complete sample data.
Save this as: orders/management/commands/import_data.py
Run with: python manage.py import_data
"""

from django.core.management.base import BaseCommand
from orders.models import Menu, Category, MenuItem, Order, OrderItem, Payment
from datetime import datetime
from decimal import Decimal


class Command(BaseCommand):
    help = 'Import complete restaurant sample data'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING('Starting data import...'))

        # Clear existing data
        self.stdout.write('Clearing existing data...')
        Payment.objects.all().delete()
        OrderItem.objects.all().delete()
        Order.objects.all().delete()
        MenuItem.objects.all().delete()
        Category.objects.all().delete()
        Menu.objects.all().delete()

        # Import Menus
        self.stdout.write('Importing menus...')
        Menu.objects.create(menu_id=1, menu_name='Food')
        Menu.objects.create(menu_id=2, menu_name='Drinks')

        # Import Categories
        self.stdout.write('Importing categories...')
        Category.objects.create(cat_id=1, category_name='Starters', menu_id=1)
        Category.objects.create(cat_id=2, category_name='Soft Drinks', menu_id=2)
        Category.objects.create(cat_id=3, category_name='Mains', menu_id=1)
        Category.objects.create(cat_id=4, category_name='Desserts', menu_id=2)
        Category.objects.create(cat_id=5, category_name='Hot Drinks', menu_id=2)

        # Import Menu Items
        # Import Menu Items
        self.stdout.write('Importing menu items...')
        MenuItem.objects.create(item_id=1, item_name='Item1', category_id=1, menu_id=1,
                                size='Small, Large', price='1.50, 2.50')
        MenuItem.objects.create(item_id=2, item_name='Item2', category_id=1, menu_id=1,
                                size='', price='3')
        MenuItem.objects.create(item_id=3, item_name='Item3', category_id=2, menu_id=2,
                                size='', price='2.5')
        MenuItem.objects.create(item_id=4, item_name='Item4', category_id=2, menu_id=2,
                                size='', price='1.5')
        MenuItem.objects.create(item_id=5, item_name='Item5', category_id=2, menu_id=1,
                                size='', price='1')
        MenuItem.objects.create(item_id=6, item_name='Item6', category_id=3, menu_id=1,
                                size='Small, Large', price='2.50, 3.6')
        MenuItem.objects.create(item_id=7, item_name='Item7', category_id=3, menu_id=1,
                                size='', price='2.5')
        MenuItem.objects.create(item_id=8, item_name='Item8', category_id=4, menu_id=2,
                                size='Small, Large', price='3.75, 6.5')
        MenuItem.objects.create(item_id=9, item_name='Item9', category_id=4, menu_id=2,
                                size='', price='1.5')
        MenuItem.objects.create(item_id=10, item_name='Item10', category_id=5, menu_id=2,
                                size='', price='2')

        # Import Orders and Order Items
        self.stdout.write('Importing orders and order items...')

        # Order History Data (All 53 records)
        order_items_data = [
            # Order 10
            (10, '2025-10-01', 2, '', '2.5', 1),
            (10, '2025-10-01', 3, '', '1.5', 2),
            (10, '2025-10-01', 1, 'Small', '3.75', 1),

            # Order 11
            (11, '2025-10-01', 5, '', '2.75', 1),
            (11, '2025-10-01', 6, '', '1.75', 2),
            (11, '2025-10-01', 2, '', '2.5', 1),
            (11, '2025-10-01', 3, '', '3.5', 1),
            (11, '2025-10-01', 4, '', '3.75', 2),
            (11, '2025-10-01', 5, '', '1.5', 1),

            # Order 12
            (12, '2025-10-01', 6, 'Large', '5.5', 2),
            (12, '2025-10-01', 7, '', '2.5', 1),
            (12, '2025-10-01', 1, 'Large', '3.5', 1),

            # Order 13
            (13, '2025-10-01', 1, 'Small', '2.75', 2),
            (13, '2025-10-01', 6, 'Small', '1.5', 1),
            (13, '2025-10-01', 8, 'Small', '3.5', 1),
            (13, '2025-10-01', 1, 'Small', '2.5', 2),

            # Order 14
            (14, '2025-10-01', 6, 'Large', '2.75', 1),
            (14, '2025-10-01', 1, 'Large', '2.75655', 2),
            (14, '2025-10-01', 8, 'Large', '2.75', 2),
            (14, '2025-10-01', 1, 'Large', '2.7556', 2),
            (14, '2025-10-01', 4, '', '5.5', 1),
            (14, '2025-10-01', 3, '', '2.75', 2),
            (14, '2025-10-01', 2, '', '3.5', 1),
            (14, '2025-10-01', 6, 'Large', '3.015', 3),

            # Order 15
            (15, '2025-10-02', 2, '', '2.568', 2),

            # Order 16
            (16, '2025-10-03', 6, 'Large', '6.586', 3),

            # Order 17
            (17, '2025-10-01', 10, '', '2.5', 1),
            (17, '2025-10-01', 9, '', '2.75636', 1),
            (17, '2025-10-01', 7, '', '5.63982', 1),

            # Order 18
            (18, '2025-10-05', 1, 'Small', '2.5698', 2),
            (18, '2025-10-05', 6, 'Small', '5.36245', 2),
            (18, '2025-10-05', 8, 'Small', '5.23569', 2),

            # Order 19
            (19, '2025-10-01', 2, '', '2.75698', 1),
            (19, '2025-10-01', 4, '', '2.356', 1),
            (19, '2025-10-01', 5, '', '2.457', 2),
            (19, '2025-10-01', 7, '', '2.6359', 1),
            (19, '2025-10-01', 9, '', '6.523', 1),
            (19, '2025-10-01', 10, '', '8.5412', 3),
            (19, '2025-10-01', 6, 'Large', '5.683', 2),
            (19, '2025-10-01', 2, '', '6.3564', 1),
            (19, '2025-10-01', 5, '', '7.235', 1),
            (19, '2025-10-01', 7, '', '2.365', 1),

            # Order 20
            (20, '2025-10-01', 1, 'Large', '2.3658', 1),
            (20, '2025-10-01', 3, '', '2.356', 1),
            (20, '2025-10-01', 6, 'Large', '1.256', 1),
            (20, '2025-10-01', 4, '', '2.635', 1),
            (20, '2025-10-01', 5, '', '5.21', 1),
            (20, '2025-10-01', 7, '', '6.325', 2),
            (20, '2025-10-01', 8, 'Small', '7.2514', 1),
            (20, '2025-10-01', 9, '', '2.3999', 1),
            (20, '2025-10-01', 4, '', '2.356', 3),
            (20, '2025-10-01', 6, 'Small', '4.5326', 2),
        ]

        # Create orders and items
        orders_dict = {}
        for order_id, order_date, item_id, size, price, qty in order_items_data:
            # Create order if not exists
            if order_id not in orders_dict:
                order = Order.objects.create(
                    order_id=order_id,
                    order_date=datetime.strptime(order_date, '%Y-%m-%d').date(),
                    order_status='Completed'
                )
                orders_dict[order_id] = order
            else:
                order = orders_dict[order_id]

            # Create order item
            OrderItem.objects.create(
                order=order,
                item_id=item_id,
                size=size if size else '',
                price=Decimal(price),
                qty=qty
            )

        # Import Payments
        self.stdout.write('Importing payments...')
        payments_data = [
            (100, 10, '2025-10-01', '9.25', 0, 0, '9.25', 'Card', 'Completed'),
            (101, 11, '2025-10-01', '21.25', 0, 0, '10', 'Cash', 'Completed'),
            (102, 11, '2025-10-01', '21.25', 0, 0, '11.25', 'Card', 'Completed'),
            (103, 12, '2025-10-02', '17', 3, 4, '16', 'Card', 'Completed'),
            (104, 13, '2025-10-03', '15.5', 0, 2, '13.5', 'Card', 'Completed'),
            (105, 14, '2025-10-01', '42.8193', 0, 0, '20', 'Cash', 'Completed'),
            (106, 14, '2025-10-01', '42.8193', 0, 0, '22.82', 'Card', 'Completed'),
            (107, 15, '2025-10-02', '5.136', 0, 0, '5.14', 'Card', 'Refunded'),
            (108, 16, '2025-10-03', '19.758', 0, 0, '10', 'Cash', 'Completed'),
            (109, 16, '2025-10-03', '19.758', 0, 0, '9.76', 'Card', 'Completed'),
            (110, 17, '2025-10-01', '10.8918', 0, 0, '10.9', 'Card', 'Completed'),
            (111, 18, '2025-10-05', '26.33588', 2, 0, '25', 'Cash', 'Completed'),
            (115, 18, '2025-10-05', '26.33588', 0, 0, '3.34', 'Card', 'Completed'),
            (116, 19, '2025-10-01', '72.13188', 0, 0, '50', 'Cash', 'Completed'),
            (119, 19, '2025-10-01', '72.13188', 0, 0, '22.13', 'Card', 'Completed'),
            (120, 20, '2025-10-01', '52.2573', 0, 0, '25', 'Cash', 'Completed'),
            (121, 20, '2025-10-01', '52.2573', 0, 0, '27.28', 'Card', 'Completed'),
        ]

        for payment_id, order_id, payment_date, amount_due, tips, discount, total_paid, payment_type, payment_status in payments_data:
            Payment.objects.create(
                payment_id=payment_id,
                order_id=order_id,
                payment_date=datetime.strptime(payment_date, '%Y-%m-%d').date(),
                amount_due=Decimal(amount_due),
                tips=Decimal(tips),
                discount=Decimal(discount),
                total_paid=Decimal(total_paid),
                payment_type=payment_type,
                payment_status=payment_status
            )

        # Summary
        self.stdout.write(self.style.SUCCESS('\n' + '='*60))
        self.stdout.write(self.style.SUCCESS('Data import completed successfully!'))
        self.stdout.write(self.style.SUCCESS('='*60))
        self.stdout.write(self.style.SUCCESS(f'✓ Menus created: {Menu.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'✓ Categories created: {Category.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'✓ Menu items created: {MenuItem.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'✓ Orders created: {Order.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'✓ Order items created: {OrderItem.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'✓ Payments created: {Payment.objects.count()}'))
        self.stdout.write(self.style.SUCCESS('='*60))

        # Show order summary
        self.stdout.write('\nOrder Summary:')
        for order in Order.objects.all().order_by('order_id'):
            item_count = order.items.count()
            payment_count = order.payments.count()
            total = order.total_amount
            self.stdout.write(
                f'  Order #{order.order_id}: {item_count} items, '
                f'{payment_count} payments, Total: ${total:.2f}'
            )