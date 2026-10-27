import urllib.parse
from decimal import Decimal
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from apps.authentication.models import User, Role
from apps.restaurants.models import Restaurant
from apps.menu.models import Category, MenuItem
from apps.tables.models import RestaurantTable, TableStatus
from apps.orders.models import Order, OrderItem, OrderType, OrderStatus
from apps.reservations.models import TableReservation, PartyBooking
from apps.customers.models import Customer
from apps.promotions.models import Offer


class ComprehensiveRestaurantAPITestCase(TestCase):
    """
    Comprehensive End-to-End Test Suite verifying all REST API endpoints
    and feature flows for the SHP Restaurant Management System.
    """

    def setUp(self):
        self.client = APIClient()
        self.restaurant = Restaurant.objects.create(
            name="SHP Restaurant",
            tagline="Good Food Great Moments",
            outlet_name="SHP Restaurant - Civil Lines",
            address="Plot 14, Main Boulevard, Civil Lines, City",
            phone="+91 98765 43210",
            email="contact@shprestaurant.com",
            gst_rate="5%",
            auto_accept=True
        )
        self.admin_user = User.objects.create_user(
            username="admin@restaurant.com",
            email="admin@restaurant.com",
            password="adminpassword123",
            name="Executive Admin",
            role=Role.ADMIN,
            restaurant=self.restaurant
        )
        self.category_pizza = Category.objects.create(name="Pizza", display_order=1)
        self.category_beverages = Category.objects.create(name="Beverages", display_order=2)
        
        self.pizza_item = MenuItem.objects.create(
            name="Truffle Mushroom Pizza",
            price=Decimal('349.00'),
            category=self.category_pizza,
            description="Wild forest mushrooms, black truffle oil",
            prep_time="20 mins",
            rating=Decimal('4.9'),
            is_veg=True,
            is_special=True,
            is_in_stock=True
        )
        self.beverage_item = MenuItem.objects.create(
            name="Matcha Citrus Sparkler",
            price=Decimal('169.00'),
            category=self.category_beverages,
            description="Ceremonial matcha with fresh Yuzu",
            prep_time="5 mins",
            rating=Decimal('4.6'),
            is_veg=True,
            is_special=False,
            is_in_stock=True
        )
        self.table_1 = RestaurantTable.objects.create(
            table_number=1,
            seats=4,
            status=TableStatus.AVAILABLE,
            floor_zone="Main Dining"
        )
        self.table_2 = RestaurantTable.objects.create(
            table_number=2,
            seats=2,
            status=TableStatus.BOOKED,
            floor_zone="Rooftop"
        )
        self.customer = Customer.objects.create(
            name="Harsh Patel",
            phone="+91 98765 43210",
            email="harsh@example.com",
            tag="VIP",
            visits=14,
            total_spent_amount=Decimal('12450.00')
        )
        self.offer = Offer.objects.create(
            title="Weekend Special",
            discount="Flat 20% OFF",
            min_spend="On all orders above ₹499",
            code="SHP20",
            tag="HOT DEAL",
            is_active=True
        )

        # The API is secure-by-default; authenticate the client as staff so the
        # management-endpoint tests exercise the real (authorized) code paths.
        self._authenticate()

    def _authenticate(self):
        login_res = self.client.post('/api/auth/login', {
            'email': 'admin@restaurant.com',
            'password': 'adminpassword123'
        })
        token = login_res.data['accessToken']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        return token

    # 1. AUTH TESTS
    def test_01_auth_login_and_me(self):
        login_res = self.client.post('/api/auth/login', {
            'email': 'admin@restaurant.com',
            'password': 'adminpassword123'
        })
        self.assertEqual(login_res.status_code, status.HTTP_200_OK)
        self.assertIn('accessToken', login_res.data)
        token = login_res.data['accessToken']

        # Access /api/auth/me
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        me_res = self.client.get('/api/auth/me')
        self.assertEqual(me_res.status_code, status.HTTP_200_OK)
        self.assertEqual(me_res.data['email'], 'admin@restaurant.com')
        self.assertEqual(me_res.data['name'], 'Executive Admin')

    def test_02_auth_signup_and_refresh(self):
        signup_res = self.client.post('/api/auth/signup', {
            'name': 'Manager User',
            'email': 'manager@restaurant.com',
            'password': 'managerpassword123',
            'role': 'manager'
        })
        self.assertEqual(signup_res.status_code, status.HTTP_201_CREATED)
        self.assertIn('accessToken', signup_res.data)
        self.assertIn('refreshToken', signup_res.data)

        refresh_res = self.client.post('/api/auth/refresh', {
            'refreshToken': signup_res.data['refreshToken']
        })
        self.assertEqual(refresh_res.status_code, status.HTTP_200_OK)
        self.assertIn('accessToken', refresh_res.data)

    def test_03_auth_logout(self):
        login_res = self.client.post('/api/auth/login', {
            'email': 'admin@restaurant.com',
            'password': 'adminpassword123'
        })
        refresh_token = login_res.data['refreshToken']
        logout_res = self.client.post('/api/auth/logout', {
            'refreshToken': refresh_token
        })
        self.assertEqual(logout_res.status_code, status.HTTP_200_OK)

    # 2. RESTAURANTS TESTS
    def test_04_restaurant_get_and_update(self):
        res = self.client.get('/api/restaurants')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(len(res.data) >= 1)
        rest_id = res.data[0]['id']

        update_res = self.client.patch(f'/api/restaurants/{rest_id}', {
            'outlet_name': 'SHP Flagship - Civil Lines',
            'gst_rate': '5%'
        })
        self.assertEqual(update_res.status_code, status.HTTP_200_OK)
        self.assertEqual(update_res.data['outlet_name'], 'SHP Flagship - Civil Lines')

    # 3. MENU & CATEGORIES TESTS
    def test_05_menu_categories_and_list(self):
        cat_res = self.client.get('/api/menu/categories')
        self.assertEqual(cat_res.status_code, status.HTTP_200_OK)
        self.assertTrue(len(cat_res.data) >= 2)

        menu_res = self.client.get('/api/menu')
        self.assertEqual(menu_res.status_code, status.HTTP_200_OK)
        self.assertTrue(len(menu_res.data) >= 2)

    def test_06_menu_toggle_stock(self):
        toggle_res = self.client.patch(f'/api/menu/{self.pizza_item.id}/toggle-stock')
        self.assertEqual(toggle_res.status_code, status.HTTP_200_OK)
        self.pizza_item.refresh_from_db()
        self.assertFalse(self.pizza_item.is_in_stock)

    def test_07_menu_item_filters(self):
        search_res = self.client.get('/api/menu?search=Truffle')
        self.assertEqual(search_res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(search_res.data), 1)

        veg_res = self.client.get('/api/menu?veg_only=true')
        self.assertEqual(veg_res.status_code, status.HTTP_200_OK)
        self.assertTrue(all(item['is_veg'] for item in veg_res.data))

    # 4. TABLES & FLOOR LAYOUT TESTS
    def test_08_tables_list_and_status_cycle(self):
        tables_res = self.client.get('/api/tables')
        self.assertEqual(tables_res.status_code, status.HTTP_200_OK)
        self.assertTrue(len(tables_res.data) >= 2)

        cycle_res = self.client.patch(f'/api/tables/{self.table_1.id}', {
            'status': 'Booked'
        })
        self.assertEqual(cycle_res.status_code, status.HTTP_200_OK)
        self.assertEqual(cycle_res.data['status'], 'Booked')

    # 5. ORDERS & DELIVERY TESTS
    def test_09_dine_in_order_flow(self):
        create_res = self.client.post('/api/orders', {
            'order_type': 'Dine In',
            'customer_name': 'Karan M.',
            'customer_phone': '+91 99887 76655',
            'table_name': 'Table 1',
            'raw_items': [
                {'menuItemId': self.pizza_item.id, 'quantity': 1},
                {'menuItemId': self.beverage_item.id, 'quantity': 2}
            ]
        }, format='json')
        self.assertEqual(create_res.status_code, status.HTTP_201_CREATED)
        order_id = create_res.data['id']
        self.assertIn('total_amount', create_res.data)

        # Update order status: New -> Preparing -> Ready -> Completed
        encoded_id = urllib.parse.quote(order_id, safe='')
        status_res = self.client.patch(f'/api/orders/{encoded_id}/status', {'status': 'Preparing'})
        self.assertEqual(status_res.status_code, status.HTTP_200_OK)
        self.assertEqual(status_res.data['status'], 'Preparing')

    def test_10_delivery_order_flow(self):
        delivery_res = self.client.post('/api/orders', {
            'order_type': 'Delivery',
            'customer_name': 'Sneha Roy',
            'customer_phone': '+91 98111 22334',
            'delivery_address': 'Flat 302, Green Park',
            'delivery_instructions': 'Ring doorbell',
            'raw_items': [
                {'menuItemId': self.pizza_item.id, 'quantity': 2}
            ]
        }, format='json')
        self.assertEqual(delivery_res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(delivery_res.data['id'].startswith('#DEL-') or delivery_res.data['id'].startswith('#'))

    # 6. RESERVATIONS & PARTY BOOKINGS TESTS
    def test_11_table_reservation(self):
        res = self.client.post('/api/reservations/table-reservations', {
            'name': 'Pooja Sharma',
            'phone': '+91 98765 11111',
            'date': '2026-09-12',
            'timeSlot': '08:00 PM',
            'guests': 2,
            'seatingZone': 'Rooftop Terrace',
            'specialRequest': 'Window table'
        })
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['name'], 'Pooja Sharma')

        list_res = self.client.get('/api/reservations/table-reservations')
        self.assertEqual(list_res.status_code, status.HTTP_200_OK)
        self.assertTrue(len(list_res.data) >= 1)

    def test_12_party_booking(self):
        res = self.client.post('/api/reservations/party-bookings', {
            'occasion': 'Corporate Gala',
            'client': 'TechCorp Solutions',
            'phone': '+91 98111 22334',
            'date': '2026-10-20',
            'guestCount': '50 People',
            'requirements': 'Private Hall & Catering'
        })
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['occasion'], 'Corporate Gala')

        list_res = self.client.get('/api/reservations/party-bookings')
        self.assertEqual(list_res.status_code, status.HTTP_200_OK)
        self.assertTrue(len(list_res.data) >= 1)

    # 7. CUSTOMERS & OFFERS TESTS
    def test_13_customers_list_and_offers(self):
        cust_res = self.client.get('/api/customers')
        self.assertEqual(cust_res.status_code, status.HTTP_200_OK)
        self.assertTrue(len(cust_res.data) >= 1)

        offers_res = self.client.get('/api/offers')
        self.assertEqual(offers_res.status_code, status.HTTP_200_OK)
        self.assertTrue(len(offers_res.data) >= 1)
        self.assertEqual(offers_res.data[0]['code'], 'SHP20')

    # 8. ANALYTICS & CSV EXPORT TESTS
    def test_14_analytics_dashboard_and_export(self):
        dash_res = self.client.get('/api/reports/dashboard')
        self.assertEqual(dash_res.status_code, status.HTTP_200_OK)
        self.assertIn('stats', dash_res.data)
        self.assertIn('reports', dash_res.data)

        csv_res = self.client.get('/api/reports/export-csv')
        self.assertEqual(csv_res.status_code, status.HTTP_200_OK)
        self.assertEqual(csv_res['Content-Type'], 'text/csv')
        self.assertIn('Order ID', str(csv_res.content))

    # 8b. SECURITY / AUTHORIZATION BOUNDARY TESTS
    def test_16_anonymous_access_boundaries(self):
        anon = APIClient()  # no credentials

        # Public reads are allowed.
        self.assertEqual(anon.get('/api/menu').status_code, status.HTTP_200_OK)
        self.assertEqual(anon.get('/api/offers').status_code, status.HTTP_200_OK)
        self.assertEqual(anon.get('/api/restaurants').status_code, status.HTTP_200_OK)

        # Protected reads are rejected for anonymous callers.
        self.assertEqual(anon.get('/api/customers').status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(anon.get('/api/orders').status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(anon.get('/api/tables').status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(anon.get('/api/reports/dashboard').status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(anon.get('/api/reports/export-csv').status_code, status.HTTP_401_UNAUTHORIZED)

    def test_17_anonymous_can_place_order_but_not_manage(self):
        anon = APIClient()
        create_res = anon.post('/api/orders', {
            'order_type': 'Delivery',
            'customer_name': 'Guest',
            'raw_items': [{'menuItemId': self.pizza_item.id, 'quantity': 1}],
        }, format='json')
        self.assertEqual(create_res.status_code, status.HTTP_201_CREATED)
        order_id = create_res.data['id']

        # Anonymous callers cannot change order status.
        encoded_id = urllib.parse.quote(order_id, safe='')
        status_res = anon.patch(f'/api/orders/{encoded_id}/status', {'status': 'Completed'})
        self.assertEqual(status_res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_18_payment_status_is_not_client_writable(self):
        # A client must not be able to mark an order paid by writing the field directly.
        order = Order.objects.create(
            restaurant=self.restaurant,
            customer_name="Fraud Attempt",
            order_type=OrderType.DELIVERY,
            total_amount=Decimal('500.00'),
        )
        encoded_id = urllib.parse.quote(order.id, safe='')
        res = self.client.patch(
            f'/api/orders/{encoded_id}',
            {'payment_status': 'Paid', 'status': 'Completed'},
            format='json',
        )
        # Request may succeed structurally, but the read-only fields must be ignored.
        order.refresh_from_db()
        self.assertEqual(order.payment_status, 'Pending')
        self.assertNotEqual(order.status, 'Completed')

    def test_19_payment_verification_requires_signature(self):
        order = Order.objects.create(
            restaurant=self.restaurant,
            customer_name="Guest",
            order_type=OrderType.DELIVERY,
            total_amount=Decimal('500.00'),
        )
        anon = APIClient()
        # Missing signature fields -> rejected, order stays unpaid.
        res = anon.post('/api/orders/verify-razorpay-payment', {
            'order_id': order.id,
            'razorpay_payment_id': 'pay_fake',
        }, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        order.refresh_from_db()
        self.assertEqual(order.payment_status, 'Pending')

    # 9. DJANGO ADMIN VIEWS VERIFICATION
    def test_15_admin_changelist_views(self):
        superuser = User.objects.create_superuser(
            username="super@restaurant.com",
            email="super@restaurant.com",
            password="superpassword123",
            name="Super Admin",
            role=Role.ADMIN,
            is_staff=True,
            is_superuser=True
        )
        # Create full sample data for all models
        order = Order.objects.create(
            restaurant=self.restaurant,
            customer_name="Test Customer",
            customer_phone="+91 99999 88888",
            order_type=OrderType.DINE_IN,
            table=self.table_1,
            table_name="Table 1",
            status=OrderStatus.PREPARING,
            total_amount=Decimal('518.00')
        )
        OrderItem.objects.create(
            order=order,
            menu_item=self.pizza_item,
            quantity=1,
            unit_price=Decimal('349.00')
        )
        TableReservation.objects.create(
            name="Test Reservation",
            phone="+91 98765 00000",
            date="2026-09-22",
            time="07:30 PM",
            guests=4,
            area="Indoor AC",
            assigned_table=self.table_1,
            status="Confirmed"
        )
        PartyBooking.objects.create(
            occasion="Birthday Party",
            client="Alice Wonderland",
            phone="+91 98765 22222",
            date="2026-10-15",
            guests="25 Guests",
            requirements="Cake & Balcony",
            status="Confirmed"
        )

        self.client.force_login(superuser)
        admin_urls = [
            '/admin/',
            '/admin/authentication/user/',
            f'/admin/authentication/user/{superuser.pk}/change/',
            '/admin/restaurants/restaurant/',
            f'/admin/restaurants/restaurant/{self.restaurant.pk}/change/',
            '/admin/menu/category/',
            f'/admin/menu/category/{self.category_pizza.pk}/change/',
            '/admin/menu/menuitem/',
            f'/admin/menu/menuitem/{self.pizza_item.pk}/change/',
            '/admin/tables/restauranttable/',
            f'/admin/tables/restauranttable/{self.table_1.pk}/change/',
            '/admin/orders/order/',
            f'/admin/orders/order/{order.pk}/change/',
            '/admin/orders/orderitem/',
            '/admin/reservations/tablereservation/',
            '/admin/reservations/partybooking/',
            '/admin/customers/customer/',
            f'/admin/customers/customer/{self.customer.pk}/change/',
            '/admin/promotions/offer/',
            f'/admin/promotions/offer/{self.offer.pk}/change/',
        ]
        for url in admin_urls:
            with self.subTest(url=url):
                res = self.client.get(url)
                self.assertEqual(res.status_code, 200, f"Admin URL {url} failed with status {res.status_code}")
