
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Order, OrderItem
from cart.models import Cart, CartItem
from .serializer import OrderSerializer


class PlaceOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        cart = Cart.objects.get(user=request.user)
        cart_items = cart.items.all()

        if not cart_items:
            return Response({"error": "Cart is empty"}, status=400)

        order = Order.objects.create(user=request.user)

        total_price = 0

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )

            total_price += item.product.price * item.quantity

        order.total_price = total_price
        order.save()

        # Clear cart
        cart_items.delete()

        return Response({
            "message": "Order placed successfully",
            "order_id": order.id
        })

class MyOrdersView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = Order.objects.filter(user=request.user).order_by('-created_at')
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)