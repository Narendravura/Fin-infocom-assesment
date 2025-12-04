from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Order, OrderItem, Payment, MenuItem


class OrderAPITestCase(APITestCase):
    """Test cases for Order API endpoints"""

    def setUp(self):
        """Set up test data"""
        # Create test data here
        pass

    def test_order_list(self):
        """Test order list endpoint"""
        response = self.client.get('/api/orders/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)



    def test_order_statistics(self):
        """Test statistics endpoint"""
        response = self.client.get('/api/orders/statistics/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)