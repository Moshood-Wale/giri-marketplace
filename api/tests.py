# tests.py
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from .models import Artisan, Product, Order
import uuid

User = get_user_model()

class ArtisanTests(APITestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123',
            name='Test User'
        )
        # Authenticate
        self.client.force_authenticate(user=self.user)
        
    def test_create_artisan(self):
        url = reverse('artisan-list')
        data = {
            'business_name': 'Test Craft Shop',
            'description': 'Test Description',
            'location': 'Test Location'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Artisan.objects.count(), 1)
        self.assertEqual(Artisan.objects.get().business_name, 'Test Craft Shop')

    def test_list_artisans(self):
        url = reverse('artisan-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)  # Check pagination

class ProductTests(APITestCase):
    def setUp(self):
        # Create user and artisan
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123',
            name='Test User'
        )
        self.client.force_authenticate(user=self.user)
        self.artisan = Artisan.objects.create(
            user=self.user,
            business_name='Test Shop',
            description='Test Description',
            location='Test Location'
        )

    def test_create_product(self):
        url = reverse('product-list')
        data = {
            'artisan': str(self.artisan.id),
            'name': 'Test Product',
            'description': 'Test Description',
            'price': '29.99',
            'inventory': 10
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 1)

    def test_filter_products(self):
        Product.objects.create(
            artisan=self.artisan,
            name='Test Product',
            description='Test Description',
            price='29.99',
            inventory=10
        )
        url = reverse('product-list')
        response = self.client.get(url, {'search': 'Test'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

class OrderTests(APITestCase):
    def setUp(self):
        # Create user, artisan, and product
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123',
            name='Test User'
        )
        self.client.force_authenticate(user=self.user)
        self.artisan = Artisan.objects.create(
            user=self.user,
            business_name='Test Shop',
            description='Test Description',
            location='Test Location'
        )
        self.product = Product.objects.create(
            artisan=self.artisan,
            name='Test Product',
            description='Test Description',
            price='29.99',
            inventory=10
        )

    def test_create_order(self):
        url = reverse('order-list')
        data = {
            'items': [{
                'product': str(self.product.id),
                'quantity': 2,
                'price': '29.99'
            }],
            'total_amount': '59.98',
            'status': 'pending'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 1)

    def test_list_user_orders(self):
        url = reverse('order-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)  # Check pagination

class AuthenticationTests(APITestCase):
    def test_user_registration(self):
        url = reverse('register')
        data = {
            'email': 'test@example.com',
            'name': 'Test User',
            'password': 'testpass123',
            'password_confirm': 'testpass123'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('tokens', response.data['data'])