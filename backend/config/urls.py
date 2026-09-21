from django.contrib import admin
from django.urls import path, re_path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

from apps.restaurants.views import RestaurantViewSet
from apps.menu.views import CategoryViewSet, MenuItemViewSet
from apps.tables.views import TableViewSet
from apps.orders.views import OrderViewSet
from apps.reservations.views import TableReservationViewSet, PartyBookingViewSet
from apps.customers.views import CustomerViewSet
from apps.promotions.views import OfferViewSet

router = DefaultRouter(trailing_slash=False)
router.register(r'restaurants', RestaurantViewSet, basename='restaurant')
router.register(r'menu/categories', CategoryViewSet, basename='category')
router.register(r'menu', MenuItemViewSet, basename='menu')
router.register(r'tables', TableViewSet, basename='table')
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'reservations/table-reservations', TableReservationViewSet, basename='table-reservation')
router.register(r'reservations/party-bookings', PartyBookingViewSet, basename='party-booking')
router.register(r'customers', CustomerViewSet, basename='customer')
router.register(r'offers', OfferViewSet, basename='offer')

urlpatterns = [
    path('admin/', admin.site.urls),

    # Auth & Custom Endpoints
    re_path(r'^api/auth/?', include('apps.authentication.urls')),
    re_path(r'^api/reports/?', include('apps.analytics.urls')),

    # REST Router Endpoints
    re_path(r'^api/?', include(router.urls)),

    # OpenAPI Schema & Interactive Docs
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
