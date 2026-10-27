import logging
from decimal import Decimal
from django.conf import settings
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import razorpay

from apps.authentication.permissions import PublicActionsOrAuthenticated
from .models import Order, PaymentStatus, OrderStatus
from .serializers import OrderSerializer

logger = logging.getLogger(__name__)


def _razorpay_client():
    """Return a configured Razorpay client, or None if keys are not set."""
    key_id = getattr(settings, 'RAZORPAY_KEY_ID', '')
    key_secret = getattr(settings, 'RAZORPAY_KEY_SECRET', '')
    if not key_id or not key_secret:
        return None
    return razorpay.Client(auth=(key_id, key_secret))


def _broadcast_order(order):
    """Push a live order update to the restaurant's KDS/POS WebSocket group."""
    try:
        channel_layer = get_channel_layer()
        if channel_layer is None:
            return
        group = f"restaurant_{order.restaurant_id or 'default'}"
        async_to_sync(channel_layer.group_send)(
            group,
            {
                'type': 'broadcast_event',
                'event_type': 'order.updated',
                'payload': OrderSerializer(order).data,
            }
        )
    except Exception:
        logger.exception('Failed to broadcast order %s over WebSocket', order.id)


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().prefetch_related('items__menu_item')
    serializer_class = OrderSerializer
    permission_classes = [PublicActionsOrAuthenticated]
    # Customers may place orders and drive their own checkout/tracking; staff
    # manage everything else (listing, status changes, edits, deletion).
    public_actions = ['create', 'retrieve', 'create_razorpay_order', 'verify_razorpay_payment']
    lookup_field = 'pk'
    lookup_value_regex = r'[^/]+'

    def get_queryset(self):
        queryset = super().get_queryset()
        order_type = self.request.query_params.get('type')
        status_param = self.request.query_params.get('status')

        if order_type and order_type != 'All':
            queryset = queryset.filter(order_type=order_type)
        if status_param and status_param != 'All':
            queryset = queryset.filter(status=status_param)

        return queryset

    @action(detail=True, methods=['patch'], url_path='status')
    def update_status(self, request, pk=None):
        order = self.get_object()
        new_status = request.data.get('status')
        valid_statuses = {choice[0] for choice in OrderStatus.choices}
        if not new_status:
            return Response(
                {'detail': 'Status field is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if new_status not in valid_statuses:
            return Response(
                {'detail': f'Invalid status. Must be one of: {", ".join(sorted(valid_statuses))}.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        order.status = new_status
        order.save(update_fields=['status', 'updated_at'])
        _broadcast_order(order)
        return Response(OrderSerializer(order).data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_path='create-razorpay-order')
    def create_razorpay_order(self, request):
        """Create a Razorpay Order for online checkout, priced from the server-side order total."""
        order_id = request.data.get('order_id')
        currency = request.data.get('currency', 'INR')

        # Price from the persisted order total, never from client-supplied amount.
        order = None
        if order_id:
            try:
                order = Order.objects.get(id=order_id)
            except Order.DoesNotExist:
                return Response({'error': 'Order not found.'}, status=status.HTTP_404_NOT_FOUND)

        amount = order.total_amount if order else request.data.get('amount')
        if not amount or Decimal(str(amount)) <= 0:
            return Response({'error': 'A valid order amount is required.'}, status=status.HTTP_400_BAD_REQUEST)

        amount_paise = int(Decimal(str(amount)) * 100)

        client = _razorpay_client()
        if client is None:
            return Response(
                {'error': 'Payment gateway is not configured.'},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

        try:
            rzp_order = client.order.create(data={
                'amount': amount_paise,
                'currency': currency,
                'receipt': str(order_id or f"rcpt_{amount_paise}"),
                'payment_capture': 1,
            })
            rzp_order_id = rzp_order['id']
        except Exception:
            logger.exception('Razorpay order creation failed')
            return Response(
                {'error': 'Could not initiate payment. Please try again.'},
                status=status.HTTP_502_BAD_GATEWAY
            )

        if order:
            order.razorpay_order_id = rzp_order_id
            order.payment_method = 'Razorpay'
            order.save(update_fields=['razorpay_order_id', 'payment_method', 'updated_at'])

        return Response({
            'razorpay_order_id': rzp_order_id,
            'amount': amount_paise,
            'currency': currency,
            'key_id': settings.RAZORPAY_KEY_ID,
        }, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_path='verify-razorpay-payment')
    def verify_razorpay_payment(self, request):
        """Verify the Razorpay signature and only then mark the order as Paid."""
        order_id = request.data.get('order_id')
        razorpay_order_id = request.data.get('razorpay_order_id')
        razorpay_payment_id = request.data.get('razorpay_payment_id')
        razorpay_signature = request.data.get('razorpay_signature')

        if not all([order_id, razorpay_order_id, razorpay_payment_id, razorpay_signature]):
            return Response(
                {'error': 'order_id, razorpay_order_id, razorpay_payment_id and razorpay_signature are all required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        client = _razorpay_client()
        if client is None:
            return Response(
                {'error': 'Payment gateway is not configured.'},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

        # Hard gate: an invalid or unverifiable signature must never mark an order paid.
        try:
            client.utility.verify_payment_signature({
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': razorpay_payment_id,
                'razorpay_signature': razorpay_signature,
            })
        except razorpay.errors.SignatureVerificationError:
            logger.warning('Razorpay signature verification failed for order %s', order_id)
            return Response(
                {'error': 'Payment signature verification failed.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception:
            logger.exception('Razorpay signature verification errored for order %s', order_id)
            return Response(
                {'error': 'Could not verify payment. Please contact support.'},
                status=status.HTTP_502_BAD_GATEWAY
            )

        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return Response({'error': 'Order not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Ensure the payment corresponds to the Razorpay order we created for this order.
        if order.razorpay_order_id and order.razorpay_order_id != razorpay_order_id:
            return Response(
                {'error': 'Payment does not match this order.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        order.payment_status = PaymentStatus.PAID
        order.payment_method = 'Razorpay Online'
        order.razorpay_order_id = razorpay_order_id
        order.razorpay_payment_id = razorpay_payment_id
        order.razorpay_signature = razorpay_signature
        order.status = OrderStatus.PREPARING
        order.save()

        _broadcast_order(order)

        return Response({
            'status': 'success',
            'message': 'Payment verified and order confirmed.',
            'order': OrderSerializer(order).data,
        }, status=status.HTTP_200_OK)
