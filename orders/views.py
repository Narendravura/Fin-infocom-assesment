from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view, throttle_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from django.core.paginator import Paginator
from django.db.models import Sum, Count, Q
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
from .models import Order, OrderItem, Payment, MenuItem, Category, Menu
from .serializers import (
    OrderDetailSerializer,
    OrderListSerializer,
    MenuItemSerializer,
    CategorySerializer,
    MenuSerializer
)


# Custom Pagination Helper
def paginate_queryset(queryset, request, page_size=10):
    """
    Paginate a queryset and return paginated response data
    """
    page = request.GET.get('page', 1)
    page_size = request.GET.get('page_size', page_size)

    try:
        page_size = int(page_size)
        if page_size > 100:
            page_size = 100
    except ValueError:
        page_size = 10

    paginator = Paginator(queryset, page_size)

    try:
        page_obj = paginator.page(page)
    except:
        page_obj = paginator.page(1)

    return {
        'count': paginator.count,
        'next': page_obj.next_page_number() if page_obj.has_next() else None,
        'previous': page_obj.previous_page_number() if page_obj.has_previous() else None,
        'results': page_obj.object_list
    }


# ==================== ORDER VIEWS ====================

@api_view(['GET'])
@cache_page(60 * 5)  # Cache for 5 minutes
@throttle_classes([AnonRateThrottle, UserRateThrottle])
def order_list(request):
    """
    List all orders with pagination and filtering.

    Query Parameters:
    - page: Page number (default: 1)
    - page_size: Items per page (default: 10, max: 100)
    - date: Filter by date (format: YYYY-MM-DD)
    - status: Filter by order status
    - date_from: Filter from date
    - date_to: Filter to date

    Returns:
    - Paginated list of orders with basic information
    """
    queryset = Order.objects.select_related().prefetch_related(
        'items__item__category',
        'payments'
    ).all()

    # Filter by date
    order_date = request.GET.get('date')
    if order_date:
        queryset = queryset.filter(order_date=order_date)

    # Filter by status
    order_status = request.GET.get('status')
    if order_status:
        queryset = queryset.filter(order_status__iexact=order_status)

    # Filter by date range
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    if date_from:
        queryset = queryset.filter(order_date__gte=date_from)
    if date_to:
        queryset = queryset.filter(order_date__lte=date_to)

    # Paginate results
    paginated_data = paginate_queryset(queryset, request)

    # Serialize results
    serializer = OrderListSerializer(paginated_data['results'], many=True)

    return Response({
        'count': paginated_data['count'],
        'next': paginated_data['next'],
        'previous': paginated_data['previous'],
        'results': serializer.data
    })


@api_view(['GET'])
@throttle_classes([AnonRateThrottle, UserRateThrottle])
def order_detail(request, order_id):
    """
    Get detailed information for a specific order.

    Args:
    - order_id: Order ID to retrieve

    Returns:
    - Complete order details including:
      - All ordered items with prices and quantities
      - All payment transactions
      - Calculated totals and balances
    """
    try:
        order = Order.objects.select_related().prefetch_related(
            'items__item__category',
            'payments'
        ).get(order_id=order_id)
    except Order.DoesNotExist:
        return Response(
            {'error': f'Order with ID {order_id} not found'},
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = OrderDetailSerializer(order)
    return Response(serializer.data)


@api_view(['GET'])
@throttle_classes([AnonRateThrottle, UserRateThrottle])
def order_search(request):
    """
    Advanced search endpoint for orders.

    Query Parameters:
    - q: Search term (searches order_id)
    - min_amount: Minimum order amount
    - max_amount: Maximum order amount
    - payment_type: Filter by payment type (Card/Cash/UPI)
    - payment_status: Filter by payment status
    - date: Filter by specific date
    - date_from: Filter from date
    - date_to: Filter to date

    Returns:
    - Paginated list of orders matching search criteria
    """
    queryset = Order.objects.select_related().prefetch_related(
        'items__item__category',
        'payments'
    ).all()

    # Search by order ID
    search_query = request.GET.get('q')
    if search_query:
        queryset = queryset.filter(order_id__icontains=search_query)

    # Filter by date
    order_date = request.GET.get('date')
    if order_date:
        queryset = queryset.filter(order_date=order_date)

    # Filter by date range
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    if date_from:
        queryset = queryset.filter(order_date__gte=date_from)
    if date_to:
        queryset = queryset.filter(order_date__lte=date_to)

    # Filter by amount range
    min_amount = request.GET.get('min_amount')
    max_amount = request.GET.get('max_amount')

    if min_amount:
        queryset = queryset.annotate(
            order_total=Sum('items__total')
        ).filter(order_total__gte=min_amount)

    if max_amount:
        if not min_amount:  # Only annotate if not already done
            queryset = queryset.annotate(order_total=Sum('items__total'))
        queryset = queryset.filter(order_total__lte=max_amount)

    # Filter by payment type
    payment_type = request.GET.get('payment_type')
    if payment_type:
        queryset = queryset.filter(
            payments__payment_type__iexact=payment_type
        ).distinct()

    # Filter by payment status
    payment_status_param = request.GET.get('payment_status')
    if payment_status_param:
        queryset = queryset.filter(
            payments__payment_status__iexact=payment_status_param
        ).distinct()

    # Paginate results
    paginated_data = paginate_queryset(queryset, request)

    # Serialize results
    serializer = OrderListSerializer(paginated_data['results'], many=True)

    return Response({
        'count': paginated_data['count'],
        'next': paginated_data['next'],
        'previous': paginated_data['previous'],
        'results': serializer.data
    })


@api_view(['GET'])
@throttle_classes([AnonRateThrottle, UserRateThrottle])
def order_statistics(request):
    """
    Get comprehensive order statistics.

    Query Parameters (optional filters):
    - date: Filter by specific date
    - date_from: Filter from date
    - date_to: Filter to date
    - status: Filter by order status

    Returns:
    - Total orders count
    - Total revenue
    - Average order value
    - Orders breakdown by status
    - Payment methods breakdown with totals
    """
    queryset = Order.objects.all()

    # Apply filters if provided
    order_date = request.GET.get('date')
    if order_date:
        queryset = queryset.filter(order_date=order_date)

    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    if date_from:
        queryset = queryset.filter(order_date__gte=date_from)
    if date_to:
        queryset = queryset.filter(order_date__lte=date_to)

    order_status_param = request.GET.get('status')
    if order_status_param:
        queryset = queryset.filter(order_status__iexact=order_status_param)

    # Calculate statistics
    total_orders = queryset.count()

    # Calculate totals
    order_stats = queryset.aggregate(
        total_revenue=Sum('items__total'),
        order_count=Count('order_id', distinct=True)
    )

    # Calculate average
    avg_order_value = None
    if order_stats['order_count'] and order_stats['order_count'] > 0:
        avg_order_value = order_stats['total_revenue'] / order_stats['order_count']

    # Orders by status
    status_breakdown = queryset.values('order_status').annotate(
        count=Count('order_id')
    ).order_by('-count')

    # Payment method breakdown
    payment_breakdown = Payment.objects.filter(
        order__in=queryset
    ).values('payment_type').annotate(
        count=Count('id'),
        total_amount=Sum('total_paid')
    ).order_by('-total_amount')

    # Payment status breakdown
    payment_status_breakdown = Payment.objects.filter(
        order__in=queryset
    ).values('payment_status').annotate(
        count=Count('id'),
        total_amount=Sum('total_paid')
    ).order_by('-count')

    return Response({
        'total_orders': total_orders,
        'total_revenue': order_stats['total_revenue'],
        'average_order_value': avg_order_value,
        'orders_by_status': list(status_breakdown),
        'payment_methods': list(payment_breakdown),
        'payment_status_breakdown': list(payment_status_breakdown)
    })

