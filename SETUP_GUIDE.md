# Restaurant Order Management API - Setup Guide

## Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Postman (for API testing)

## Step-by-Step Setup

### 1. Create Project Directory
```bash
mkdir restaurant_api
cd restaurant_api
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Create Django Project
```bash
django-admin startproject restaurant_project .
django-admin startapp orders
```

### 5. Project Structure
```
restaurant_api/
├── restaurant_project/
│   ├── __init__.py
│   ├── settings.py      # Add REST framework settings here
│   ├── urls.py          # Main URL configuration
│   └── wsgi.py
├── orders/
│   ├── management/
│   │   └── commands/
│   │       └── import_data.py  # Data import script
│   ├── __init__.py
│   ├── models.py        # Database models
│   ├── serializers.py   # API serializers
│   ├── views.py         # API views
│   ├── urls.py          # App URLs
│   └── admin.py
├── manage.py
└── requirements.txt
```

### 6. Configure URLs (restaurant_project/urls.py)
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('orders.urls')),
]
```

### 7. Update Settings
Add the REST framework and CORS configurations from `settings.py` artifact to your `restaurant_project/settings.py` file.

Add 'orders' to INSTALLED_APPS:
```python
INSTALLED_APPS = [
    # ... other apps
    'rest_framework',
    'corsheaders',
    'django_filters',
    'orders',
]
```

### 8. Create Database Tables
```bash
python manage.py makemigrations
python manage.py migrate
```

### 9. Create Superuser (Optional)
```bash
python manage.py createsuperuser
```

### 10. Import Sample Data
```bash
python manage.py import_data
```

### 11. Run Development Server
```bash
python manage.py runserver
```

Server will start at: `http://127.0.0.1:8000/`

---

## API Endpoints

### Base URL: `http://127.0.0.1:8000/api/`

### Available Endpoints:

#### 1. List All Orders (Paginated)
```
GET /api/orders/
GET /api/orders/?page=2
GET /api/orders/?page_size=20
```

#### 2. Get Specific Order Details
```
GET /api/orders/{order_id}/
Example: GET /api/orders/10/
```

#### 3. Filter Orders by Date
```
GET /api/orders/?date=2025-10-01
```

#### 4. Filter Orders by Status
```
GET /api/orders/?status=completed
```

#### 5. Filter by Date Range
```
GET /api/orders/?date_from=2025-10-01&date_to=2025-10-05
```

#### 6. Search Orders
```
GET /api/orders/search/?q=10
GET /api/orders/search/?min_amount=20&max_amount=100
GET /api/orders/search/?payment_type=Card
GET /api/orders/search/?payment_status=Completed
```

#### 7. Get Order Statistics
```
GET /api/orders/statistics/
```


---

## Postman Testing

### 1. Import Collection to Postman

Create a new collection called "Restaurant API" with these requests:

#### Request 1: Get All Orders
- **Method**: GET
- **URL**: `http://127.0.0.1:8000/api/orders/`
- **Description**: Retrieves paginated list of all orders

#### Request 2: Get Order Details
- **Method**: GET
- **URL**: `http://127.0.0.1:8000/api/orders/10/`
- **Description**: Get complete details for Order #10

#### Request 3: Search by Date
- **Method**: GET
- **URL**: `http://127.0.0.1:8000/api/orders/?date=2025-10-01`

#### Request 4: Get Statistics
- **Method**: GET
- **URL**: `http://127.0.0.1:8000/api/orders/statistics/`

#### Request 5: Advanced Search
- **Method**: GET
- **URL**: `http://127.0.0.1:8000/api/orders/search/?payment_type=Card&min_amount=20`

### 2. Expected Response Format

#### List Orders Response:
```json
{
    "count": 10,
    "next": "http://127.0.0.1:8000/api/orders/?page=2",
    "previous": null,
    "results": [
        {
            "order_id": 10,
            "order_date": "2025-10-01",
            "order_status": "Completed",
            "item_count": 3,
            "payment_count": 1,
            "total_amount": "9.25",
            "total_paid": "9.25",
            "created_at": "2025-10-01T10:30:00Z"
        }
    ]
}
```

#### Order Detail Response:
```json
{
    "order_id": 10,
    "order_date": "2025-10-01",
    "order_status": "Completed",
    "item_count": 3,
    "total_amount": "9.25",
    "total_paid": "9.25",
    "payment_balance": "0.00",
    "items": [
        {
            "id": 1,
            "item_id": 2,
            "item_name": "Item2",
            "category_name": "Starters",
            "size": "",
            "price": "2.50000",
            "qty": 1,
            "total": "2.50000"
        },
        {
            "id": 2,
            "item_id": 3,
            "item_name": "Item3",
            "category_name": "Soft Drinks",
            "size": "",
            "price": "1.50000",
            "qty": 2,
            "total": "3.00000"
        },
        {
            "id": 3,
            "item_id": 1,
            "item_name": "Item1",
            "category_name": "Starters",
            "size": "Small",
            "price": "3.75000",
            "qty": 1,
            "total": "3.75000"
        }
    ],
    "payments": [
        {
            "id": 1,
            "payment_id": 100,
            "payment_date": "2025-10-01",
            "amount_due": "9.25000",
            "tips": "0.00",
            "discount": "0.00",
            "total_paid": "9.25",
            "payment_type": "Card",
            "payment_status": "Completed"
        }
    ],
    "created_at": "2025-10-01T10:30:00Z"
}
```

---

## Security Features Implemented

### 1. **Rate Limiting**
- Anonymous users: 100 requests/hour
- Authenticated users: 1000 requests/hour

### 2. **Input Validation**
- Model-level validation using Django validators
- Serializer-level validation
- Minimum value validators for prices and quantities

### 3. **Query Optimization**
- `select_related()` for foreign keys
- `prefetch_related()` for reverse foreign keys
- Reduces database queries (N+1 problem prevention)

### 4. **Caching**
- 5-minute cache on list endpoints
- Reduces database load

### 5. **CORS Protection**
- Configured allowed origins
- Prevents unauthorized cross-origin requests

### 6. **Security Headers**
- XSS filtering enabled
- Content type nosniff
- Clickjacking protection

---

## Performance Optimizations

1. **Database Indexing**
   - Indexes on foreign keys
   - Indexes on frequently queried fields

2. **Query Optimization**
   - Eager loading of related objects
   - Pagination for large result sets

3. **Caching Strategy**
   - In-memory caching for frequently accessed data
   - Cache invalidation on updates

4. **Response Optimization**
   - Different serializers for list vs detail views
   - Minimal data in list views, full data in detail views

---

## API Documentation

### Browsable API
Visit `http://127.0.0.1:8000/api/` in your browser to access Django REST Framework's browsable API interface.

### Generate OpenAPI Schema (Optional)
```bash
pip install drf-spectacular
```

Add to settings.py:
```python
INSTALLED_APPS += ['drf_spectacular']

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}
```

Generate schema:
```bash
python manage.py spectacular --file schema.yml
```

---

## Troubleshooting

### Issue: Module not found
**Solution**: Make sure virtual environment is activated and all packages are installed

### Issue: Database errors
**Solution**: Run migrations again
```bash
python manage.py makemigrations
python manage.py migrate
```

### Issue: Port already in use
**Solution**: Use different port
```bash
python manage.py runserver 8001
```

### Issue: CORS errors
**Solution**: Add your frontend URL to `CORS_ALLOWED_ORIGINS` in settings.py

---
