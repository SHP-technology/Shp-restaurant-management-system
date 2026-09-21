# SHP Restaurant Management System — Django Backend

A high-performance Django 5.x + Django REST Framework + Channels backend with JWT authentication, real-time WebSocket updates, POS & order management, table layout management, reservations, and analytics.

---

## 🚀 Quick Start

### 1. Setup Virtual Environment
```bash
python3 -m venv backend/venv
source backend/venv/bin/activate
pip install -r backend/requirements.txt
```

### 2. Run Database Migrations
```bash
python backend/manage.py migrate
```

### 3. Seed Initial Demo Data (Menu, Tables, Orders, Admin User)
```bash
python backend/manage.py seed_restaurant_data
```

**Default Admin Credentials:**
- **Email:** `admin@restaurant.com`
- **Password:** `password123`

### 4. Start ASGI / HTTP Server (with WebSockets)
```bash
python backend/manage.py runserver 8000
```
or via Daphne:
```bash
daphne -p 8000 config.asgi:application
```

---

## 📖 Interactive API Documentation

- **Swagger UI:** `http://localhost:8000/api/docs/`
- **ReDoc:** `http://localhost:8000/api/redoc/`
- **OpenAPI 3.0 Schema:** `http://localhost:8000/api/schema/`

---

## 📡 Key REST Endpoints

- `POST /api/auth/login` — JWT Login
- `POST /api/auth/signup` — Register staff / outlet admin
- `GET /api/auth/me` — Active session user profile
- `GET /api/menu` — Food menu catalog & category filtering
- `GET /api/tables` — Floor layout & table status
- `PATCH /api/tables/{id}` — Update table status (`Available`, `Booked`, `Occupied`)
- `GET /api/orders` — POS, Dine-in & Doorstep delivery orders
- `POST /api/orders` — Create order
- `PATCH /api/orders/{id}/status` — Advance order state (`Preparing`, `Ready`, `Delivered`, `Completed`)
- `POST /api/reservations/table-reservations` — Book a dining table
- `POST /api/reservations/party-bookings` — Party / event catering inquiry
- `GET /api/reports/dashboard` — Live revenue & KPI metrics
- `GET /api/reports/export-csv` — Download sales report CSV

---

## ⚡ WebSockets (Django Channels)

- **URL:** `ws://localhost:8000/ws/restaurant/{restaurant_id}/`
- **Events Dispatched:**
  - `order.created`
  - `order.status_updated`
  - `table.status_updated`
  - `dashboard.stats_updated`
