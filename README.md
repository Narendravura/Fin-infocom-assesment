# Restaurant Order Management API

A Django REST Framework API for managing restaurant orders, payments, and menu items.

## Quick Start

1. Create virtual environment: `python -m venv venv`
2. Activate: `source venv/bin/activate` (Linux/Mac) or `venv\Scripts\activate` (Windows)
3. Install dependencies: `pip install -r requirements.txt`
4. Run migrations: `python manage.py migrate`
5. Import data: `python manage.py import_data`
6. Run server: `python manage.py runserver`

## API Endpoints

- `GET /api/orders/` - List all orders
- `GET /api/orders/{id}/` - Order details
- `GET /api/orders/search/` - Search orders
- `GET /api/orders/statistics/` - Statistics

See SETUP_GUIDE.md for detailed documentation.