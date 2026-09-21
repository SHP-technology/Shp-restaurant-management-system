from django.core.management.base import BaseCommand
from apps.authentication.models import User, Role
from apps.restaurants.models import Restaurant
from apps.menu.models import Category, MenuItem
from apps.tables.models import RestaurantTable, TableStatus
from apps.orders.models import Order, OrderItem, OrderType, OrderStatus
from apps.reservations.models import TableReservation, PartyBooking
from apps.customers.models import Customer
from apps.promotions.models import Offer


class Command(BaseCommand):
    help = 'Seeds database with initial SHP restaurant data, admin user, menu catalog, tables and demo orders.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE('Seeding SHP Restaurant Database...'))

        # 1. Restaurant
        restaurant, created = Restaurant.objects.get_or_create(
            outlet_name='SHP Restaurant - Civil Lines',
            defaults={
                'name': 'SHP Restaurant',
                'tagline': 'Good Food Great Moments',
                'description': 'Delicious food, your way — dine in, delivery or celebration, we’ve got you covered.',
                'hero_image': 'https://images.unsplash.com/photo-1555396273-367ea4eb4db5?auto=format&fit=crop&w=1000&q=80',
                'address': 'Plot 14, Main Boulevard, Civil Lines, City',
                'phone': '+91 98765 43210 / 011 2345 6789',
                'email': 'contact@shprestaurant.com',
                'opening_hours': 'Mon - Sun: 11:00 AM – 11:30 PM',
                'gst_rate': '5%',
                'auto_accept': True,
            }
        )

        # 2. Users
        if not User.objects.filter(email='admin@restaurant.com').exists():
            admin_user = User.objects.create_superuser(
                username='admin@restaurant.com',
                email='admin@restaurant.com',
                password='password123',
                name='Restaurant Admin',
                role=Role.ADMIN,
                restaurant=restaurant,
            )
            self.stdout.write(self.style.SUCCESS(f'Created Admin User: {admin_user.email} (pass: password123)'))

        # 3. Categories & Menu Items
        cat_data = [
            ('Pizza', 'https://images.unsplash.com/photo-1574071318508-1cdbab80d002?auto=format&fit=crop&w=500&q=80'),
            ('Burgers', 'https://images.unsplash.com/photo-1568901346375-23c9450c58cd?auto=format&fit=crop&w=500&q=80'),
            ('Asian', 'https://images.unsplash.com/photo-1585032226651-759b368d7246?auto=format&fit=crop&w=500&q=80'),
            ('Indian', 'https://images.unsplash.com/photo-1563379091339-03246963d51a?auto=format&fit=crop&w=500&q=80'),
            ('Beverages', 'https://images.unsplash.com/photo-1544145945-f90425340c7e?auto=format&fit=crop&w=500&q=80'),
            ('Desserts', 'https://images.unsplash.com/photo-1551024506-0bccd828d307?auto=format&fit=crop&w=500&q=80'),
        ]
        categories = {}
        for idx, (cname, cimg) in enumerate(cat_data):
            cat, _ = Category.objects.get_or_create(
                name=cname,
                defaults={'image': cimg, 'display_order': idx + 1}
            )
            categories[cname] = cat

        dishes = [
            {
                'id': 1,
                'name': 'Truffle Mushroom Pizza',
                'price': 349,
                'category': categories['Pizza'],
                'description': 'Wild forest mushrooms, black truffle oil, fresh mozzarella, and aromatic basil.',
                'rating': 4.9,
                'prep_time': '20 mins',
                'is_veg': True,
                'is_special': True,
                'image': 'https://images.unsplash.com/photo-1574071318508-1cdbab80d002?auto=format&fit=crop&w=600&q=80',
                'is_in_stock': True,
            },
            {
                'id': 2,
                'name': 'Artisan Smash Burger',
                'price': 279,
                'category': categories['Burgers'],
                'description': 'Double smashed patty, aged cheddar, caramelised onions, brioche bun, signature sauce.',
                'rating': 4.8,
                'prep_time': '15 mins',
                'is_veg': False,
                'is_special': True,
                'image': 'https://images.unsplash.com/photo-1568901346375-23c9450c58cd?auto=format&fit=crop&w=600&q=80',
                'is_in_stock': True,
            },
            {
                'id': 3,
                'name': 'Spicy Schezwan Noodles',
                'price': 249,
                'category': categories['Asian'],
                'description': 'Wok-tossed hand-pulled noodles with crisp vegetables and chili schezwan glaze.',
                'rating': 4.7,
                'prep_time': '18 mins',
                'is_veg': True,
                'is_special': False,
                'image': 'https://images.unsplash.com/photo-1585032226651-759b368d7246?auto=format&fit=crop&w=600&q=80',
                'is_in_stock': True,
            },
            {
                'id': 4,
                'name': 'Burrata Margherita Pizza',
                'price': 389,
                'category': categories['Pizza'],
                'description': 'Creamy San Marzano tomato sauce, fresh creamy burrata ball, micro basil.',
                'rating': 4.9,
                'prep_time': '22 mins',
                'is_veg': True,
                'is_special': False,
                'image': 'https://images.unsplash.com/photo-1579751626657-72bc17010498?auto=format&fit=crop&w=600&q=80',
                'is_in_stock': True,
            },
            {
                'id': 5,
                'name': 'Dum Pukht Veg Biryani',
                'price': 299,
                'category': categories['Indian'],
                'description': 'Aromatic long-grain basmati, saffron, seasonal vegetables sealed in clay pot.',
                'rating': 4.8,
                'prep_time': '25 mins',
                'is_veg': True,
                'is_special': False,
                'image': 'https://images.unsplash.com/photo-1563379091339-03246963d51a?auto=format&fit=crop&w=600&q=80',
                'is_in_stock': True,
            },
            {
                'id': 6,
                'name': 'Matcha Citrus Sparkler',
                'price': 169,
                'category': categories['Beverages'],
                'description': 'Ceremonial matcha whisked with fresh Yuzu juice, mint, and sparkling soda.',
                'rating': 4.6,
                'prep_time': '5 mins',
                'is_veg': True,
                'is_special': False,
                'image': 'https://images.unsplash.com/photo-1544145945-f90425340c7e?auto=format&fit=crop&w=600&q=80',
                'is_in_stock': False,
            },
            {
                'id': 7,
                'name': 'Molten Belgian Chocolate Lava',
                'price': 219,
                'category': categories['Desserts'],
                'description': 'Warm dark chocolate cake with a oozing center, served with vanilla bean ice cream.',
                'rating': 4.9,
                'prep_time': '12 mins',
                'is_veg': True,
                'is_special': False,
                'image': 'https://images.unsplash.com/photo-1551024506-0bccd828d307?auto=format&fit=crop&w=600&q=80',
                'is_in_stock': True,
            },
        ]
        menu_objs = {}
        for d in dishes:
            m_id = d.pop('id')
            obj, _ = MenuItem.objects.update_or_create(id=m_id, defaults=d)
            menu_objs[m_id] = obj

        # 4. Tables (1 to 16)
        for num in range(1, 17):
            status = TableStatus.AVAILABLE
            if num in (5, 7):
                status = TableStatus.BOOKED
            elif num in (3, 12):
                status = TableStatus.OCCUPIED
            seats = 6 if num % 3 == 0 else 4 if num % 2 == 0 else 2
            RestaurantTable.objects.update_or_create(
                table_number=num,
                defaults={'seats': seats, 'status': status}
            )

        # 5. Orders
        sample_orders = [
            {
                'id': '#1258',
                'order_type': OrderType.DINE_IN,
                'table_name': 'Table 4',
                'customer_name': 'Rahul M.',
                'status': OrderStatus.NEW,
                'total_amount': 458.00,
                'items': [(1, 1), (6, 1)],
            },
            {
                'id': '#1257',
                'order_type': OrderType.DELIVERY,
                'customer_name': 'Harsh P.',
                'customer_phone': '+91 98765 43210',
                'delivery_address': 'Flat 201, Civil Lines',
                'status': OrderStatus.PREPARING,
                'total_amount': 678.00,
                'items': [(5, 1), (7, 1)],
            },
            {
                'id': '#1256',
                'order_type': OrderType.DINE_IN,
                'table_name': 'Table 12',
                'customer_name': 'Ananya R.',
                'status': OrderStatus.READY,
                'total_amount': 249.00,
                'items': [(4, 1)],
            },
            {
                'id': '#1255',
                'order_type': OrderType.DELIVERY,
                'customer_name': 'Vikram S.',
                'customer_phone': '+91 99887 11223',
                'delivery_address': 'Sunset Towers',
                'status': OrderStatus.NEW,
                'total_amount': 689.00,
                'items': [(2, 2)],
            },
            {
                'id': '#1254',
                'order_type': OrderType.TAKEAWAY,
                'customer_name': 'Priya K.',
                'status': OrderStatus.PREPARING,
                'total_amount': 378.00,
                'items': [(3, 1)],
            },
            {
                'id': '#1253',
                'order_type': OrderType.DINE_IN,
                'table_name': 'Table 1',
                'customer_name': 'Amit K.',
                'status': OrderStatus.COMPLETED,
                'total_amount': 520.00,
                'items': [(1, 1), (7, 1)],
            },
            # Delivery order logistics
            {
                'id': '#DEL-801',
                'order_type': OrderType.DELIVERY,
                'customer_name': 'Rohan Gupta',
                'customer_phone': '+91 98765 11223',
                'delivery_address': 'Flat 302, Green Park',
                'status': OrderStatus.OUT_FOR_DELIVERY,
                'driver': 'Suresh (Rider #4)',
                'estimated_time': '20 mins left',
                'total_amount': 550.00,
                'items': [(1, 1)],
            },
            {
                'id': '#DEL-802',
                'order_type': OrderType.DELIVERY,
                'customer_name': 'Sneha Roy',
                'customer_phone': '+91 98111 22334',
                'delivery_address': 'B-12, Model Town',
                'status': OrderStatus.PREPARING,
                'driver': 'Assigning...',
                'estimated_time': '35 mins left',
                'total_amount': 380.00,
                'items': [(2, 1)],
            },
            {
                'id': '#DEL-803',
                'order_type': OrderType.DELIVERY,
                'customer_name': 'Aman Verma',
                'customer_phone': '+91 97777 88899',
                'delivery_address': 'Suite 401, Tech Hub',
                'status': OrderStatus.DELIVERED,
                'driver': 'Ramesh (Rider #1)',
                'estimated_time': 'Completed',
                'total_amount': 720.00,
                'items': [(5, 2)],
            },
        ]

        for odata in sample_orders:
            items = odata.pop('items')
            order_id = odata.pop('id')
            order, _ = Order.objects.update_or_create(
                id=order_id,
                restaurant=restaurant,
                defaults=odata
            )
            order.items.all().delete()
            for menu_id, qty in items:
                if menu_id in menu_objs:
                    m_item = menu_objs[menu_id]
                    OrderItem.objects.create(
                        order=order,
                        menu_item=m_item,
                        quantity=qty,
                        unit_price=m_item.price
                    )

        # 6. Table Reservations & Party Bookings
        res_data = [
            {'id': 'RES-101', 'name': 'Harsh Patel', 'phone': '+91 98765 43210', 'date': '28 May 2025', 'time': '7:30 PM', 'guests': '4 People', 'area': 'Indoor (Table 5)', 'status': 'Confirmed'},
            {'id': 'RES-102', 'name': 'Neha Sharma', 'phone': '+91 98123 45678', 'date': '28 May 2025', 'time': '8:15 PM', 'guests': '2 People', 'area': 'Rooftop', 'status': 'Pending'},
            {'id': 'RES-103', 'name': 'Karan Mehra', 'phone': '+91 99887 76655', 'date': '29 May 2025', 'time': '1:30 PM', 'guests': '6 People', 'area': 'VIP Booth', 'status': 'Confirmed'},
        ]
        for r in res_data:
            r_id = r.pop('id')
            TableReservation.objects.update_or_create(id=r_id, defaults=r)

        party_data = [
            {'id': 'PRT-501', 'occasion': 'Birthday Bash', 'client': 'Pooja Kapoor', 'date': '05 June 2025', 'guests': '20 People', 'requirements': 'Decoration, Cake, Music', 'status': 'Confirmed'},
            {'id': 'PRT-502', 'occasion': 'Corporate Gala', 'client': 'TechCorp Solutions', 'date': '12 June 2025', 'guests': '50 People', 'requirements': 'Private Hall & Cocktail Bar', 'status': 'Pending Inquiry'},
        ]
        for p in party_data:
            p_id = p.pop('id')
            PartyBooking.objects.update_or_create(id=p_id, defaults=p)

        # 7. Customers
        customers_data = [
            {'id': 'CUST-01', 'name': 'Harsh Patel', 'phone': '+91 98765 43210', 'visits': 14, 'total_spent_amount': 12450.00, 'tag': 'VIP'},
            {'id': 'CUST-02', 'name': 'Ananya Rao', 'phone': '+91 98123 45678', 'visits': 8, 'total_spent_amount': 6800.00, 'tag': 'Regular'},
            {'id': 'CUST-03', 'name': 'Vikram Singh', 'phone': '+91 99887 11223', 'visits': 3, 'total_spent_amount': 2350.00, 'tag': 'New'},
        ]
        for c in customers_data:
            c_id = c.pop('id')
            Customer.objects.update_or_create(id=c_id, defaults=c)

        # 8. Offers
        offers_data = [
            {'title': 'Weekend Special Offer', 'discount': 'Flat 20% OFF', 'min_spend': 'On all orders above ₹499', 'code': 'SHP20', 'tag': 'HOT DEAL', 'badge_color': 'bg-rose-500 text-white'},
            {'title': 'Welcome First Order', 'discount': '15% OFF', 'min_spend': 'On your very first order', 'code': 'WELCOME15', 'tag': 'NEW USER', 'badge_color': 'bg-[#f47b20] text-white'},
            {'title': 'Sweet Delight', 'discount': 'Free Dessert', 'min_spend': 'On orders above ₹699', 'code': 'DESSERT', 'tag': 'SPECIAL', 'badge_color': 'bg-emerald-600 text-white'},
        ]
        for o in offers_data:
            code = o.pop('code')
            Offer.objects.update_or_create(code=code, defaults=o)

        self.stdout.write(self.style.SUCCESS('Successfully seeded all SHP Restaurant records!'))
