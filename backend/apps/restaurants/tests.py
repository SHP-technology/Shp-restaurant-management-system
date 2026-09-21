from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from apps.authentication.models import User, Role
from apps.restaurants.models import Restaurant
from apps.menu.models import Category, MenuItem
from apps.tables.models import RestaurantTable, TableStatus
from apps.orders.models import Order, OrderType, OrderStatus
from apps.reservations.models import TableReservation, PartyBooking
from apps.promotions.models import Offer


class RestaurantAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.restaurant = Restaurant.objects.create(
            name="SHP Restaurant",
            outlet_name="Civil Lines"
        )
        self.admin = User.objects.create_user(
            username="testadmin@restaurant.com",
            email="testadmin@restaurant.com",
            password="password123",
            name="Test Admin",
            role=Role.ADMIN,
            restaurant=self.restaurant
        )
        self.category = Category.objects.create(name="Pizza")
        self.menu_item = MenuItem.objects.create(
            name="Truffle Mushroom Pizza",
            price=349,
            category=self.category,
            is_veg=True
        )
        self.table = RestaurantTable.objects.create(
            table_number=1,
            seats=4,
            status=TableStatus.AVAILABLE
        )

    def test_auth_login(self):
        response = self.client.post('/api/auth/login', {
            'email': 'testadmin@restaurant.com',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('accessToken', response.data)
        self.assertIn('user', response.data)
        self.assertEqual(response.data['user']['email'], 'testadmin@restaurant.com')

    def test_auth_signup(self):
        response = self.client.post('/api/auth/signup', {
            'name': 'New Staff',
            'email': 'newstaff@restaurant.com',
            'password': 'secretpassword123'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('accessToken', response.data)
        self.assertEqual(response.data['user']['name'], 'New Staff')

    def test_menu_list(self):
        response = self.client.get('/api/menu')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) >= 1)

    def test_table_status_update(self):
        response = self.client.patch(f'/api/tables/{self.table.id}', {
            'status': 'Booked'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.table.refresh_from_db()
        self.assertEqual(self.table.status, 'Booked')

    def test_order_creation_and_status_update(self):
        # Create order
        response = self.client.post('/api/orders', {
            'order_type': 'Dine In',
            'customer_name': 'Rahul M.',
            'raw_items': [
                {'menuItemId': self.menu_item.id, 'quantity': 2}
            ]
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        order_id = response.data['id']
        import urllib.parse
        encoded_id = urllib.parse.quote(order_id, safe='')
        patch_res = self.client.patch(f'/api/orders/{encoded_id}/status', {
            'status': 'Preparing'
        })
        self.assertEqual(patch_res.status_code, status.HTTP_200_OK)
        self.assertEqual(patch_res.data['status'], 'Preparing')

    def test_table_reservation(self):
        response = self.client.post('/api/reservations/table-reservations', {
            'name': 'Harsh Patel',
            'phone': '+91 98765 43210',
            'date': '2026-09-10',
            'timeSlot': '07:30 PM',
            'guests': 4,
            'seatingZone': 'Main Dining'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Harsh Patel')

    def test_party_booking(self):
        response = self.client.post('/api/reservations/party-bookings', {
            'occasion': 'Birthday Celebration',
            'clientName': 'Pooja Kapoor',
            'phone': '+91 98765 43210',
            'guestCount': '25-50 Guests',
            'date': '2026-10-15',
            'requirements': 'Music and cake'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['occasion'], 'Birthday Celebration')

    def test_analytics_dashboard_and_csv_export(self):
        dash_res = self.client.get('/api/reports/dashboard')
        self.assertEqual(dash_res.status_code, status.HTTP_200_OK)
        self.assertIn('stats', dash_res.data)

        csv_res = self.client.get('/api/reports/export-csv')
        self.assertEqual(csv_res.status_code, status.HTTP_200_OK)
        self.assertEqual(csv_res['Content-Type'], 'text/csv')
