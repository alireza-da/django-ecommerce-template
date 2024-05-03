import secrets

from django.shortcuts import render
from datetime import datetime
from django.http import HttpResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import mixins
from rest_framework import generics
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.parsers import MultiPartParser, FormParser

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from registration.models import CustomUser
from registration.serializers import CustomUserSerializer
from shop.models import Product
from shop.permissions import IsOwnerOrReadOnly
from shop.serializers import *


# Create your views here.
def mock_payment(request, *args, **kwargs):
    now = datetime.now()
    html = "<html><body>Payment Successful. Timestamp: %s.</body></html>" % now
    return HttpResponse(html)


def handler404(request, *args, **kwargs):
    return render(request, 'index.html')


# Product
class ProductCreateView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]


class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = []


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]


# Category
class CategoryCreateView(generics.CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = []


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser]


# Product Image
class ProductImageCreateView(generics.CreateAPIView):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer
    permission_classes = [IsAdminUser]


class ProductImageListView(generics.ListAPIView):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer
    permission_classes = []


class ProductImageDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer
    permission_classes = [IsAdminUser]


# Coupon
class CouponCreateView(generics.CreateAPIView):
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer
    permission_classes = [IsAdminUser]


class CouponListView(generics.ListAPIView):
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer
    permission_classes = [IsAdminUser]


class CouponDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer
    permission_classes = [IsAdminUser]

    def get(self, request, *args, **kwargs):
        try:
            coupon = Coupon.objects.get(code=self.kwargs['code'])
            return Response(data=self.serializer_class(coupon).data, status=status.HTTP_200_OK)
        except Coupon.DoesNotExist:
            return Response(data={}, status=status.HTTP_404_NOT_FOUND)
        except KeyError as e:
            return Response(data={'error': f"provide {e}"}, status=status.HTTP_401_UNAUTHORIZED)


# Payment
class PaymentCreateView(generics.CreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]


class PaymentListView(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]


class PaymentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]


class MockPayment(generics.RetrieveUpdateDestroyAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            payment = Payment.objects.create()
            total_amount = 0
            address = UserAddress.objects.get(id=request.data['address_id'])
            order = Order.objects.create(user=request.user, payment=payment, address=address)
            ois = []
            ois_payload = []
            for oi in request.data['order_items']:
                product = Product.objects.get(id=oi['id'])
                order_item = OrderItem.objects.create(product=product,
                                                      quantity=oi['quantity'],
                                                      price=product.price,
                                                      order=order
                                                      )
                total_amount += product.price
                ois.append(order_item)
                ois_payload.append(OrderItemSerializer(order_item).data)

            payment.total_amount = total_amount
            transaction = Transaction.objects.create(payment=payment)
            transaction.code = secrets.token_urlsafe()
            # TODO : make this atomic
            for oi in ois:
                oi.save()

            payment.save()
            product.save()
            order.save()
            transaction.save()
            payment_payload = self.serializer_class(payment).data
            del payment_payload['id']
            order_payload = OrderSerializer(order).data
            del order_payload['id']
            order_item_payload = OrderItemSerializer(order_item).data
            del order_item_payload['id']
            transaction_payload = TransactionSerializer(transaction).data
            del transaction_payload['id']

            data = {
                'payment': payment_payload,
                'order': order_payload,
                'order_item': ois_payload,
                'transaction': transaction_payload
            }
            return Response(data=data, status=status.HTTP_200_OK)

        except Category.DoesNotExist:
            return Response(data={'error': 'user not authorized'},
                            status=status.HTTP_401_UNAUTHORIZED)
        except Product.DoesNotExist:
            return Response(data={'error': 'product not found'}, status=status.HTTP_404_NOT_FOUND)
        except KeyError as e:
            return Response(data={'error': f'invalid request: provide {e}'},
                            status=status.HTTP_400_BAD_REQUEST)


# Order
class OrderCreateView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = []


class OrderListView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAdminUser]


class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]


class OrderUserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get(self, request, *args, **kwargs):
        try:
            orders = Order.objects.filter(user=self.request.user)
            orders_serialized = OrderSerializer(orders, many=True).data

            for order in orders_serialized:
                order_items = OrderItem.objects.filter(order_id=order['id'])
                order_items_serialized = OrderItemSerializer(order_items, many=True)
                payment = Payment.objects.get(id=order['id'])
                payment_ser = PaymentSerializer(payment, many=False)
                order['order_items'] = order_items_serialized.data
                order['payment'] = payment_ser.data

            return Response(data=orders_serialized, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response(data={'error': 'user does not exist'}, status=status.HTTP_404_NOT_FOUND)


# OrderItem
class OrderItemCreateView(generics.CreateAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = []


class OrderItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticated]


class OrderItemListView(generics.ListAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [IsAdminUser]


class OrderItemUserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get(self, request, *args, **kwargs):
        try:
            order = self.queryset.filter(user=self.request.user)
            serializer = OrderSerializer(order, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except OrderItem.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


# Transaction
class TransactionListView(generics.ListAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAdminUser]


class TransactionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]


class TransactionCreateView(generics.CreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]


class TransactionUserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a transaction of a user
    """
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get(self, request, *args, **kwargs):
        if request.user:
            try:
                transaction = Transaction.objects.filter(user=request.user)
                serializer = TransactionSerializer(transaction, many=True)
                return Response(data=serializer.data, status=status.HTTP_200_OK)
            except CustomUser.DoesNotExist:
                return Response(data="user not found", status=status.HTTP_404_NOT_FOUND)
        return Response(data="Invalid Request", status=status.HTTP_400_BAD_REQUEST)


class CategoryItemsList(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = []

    def get(self, request, *args, **kwargs):
        pds = Product.objects.filter(category_id=self.kwargs['category_id'])
        serializer = ProductSerializer(pds, many=True)
        return Response(self.serializer_class(serializer.data, many=True).data)


class CategoriesProductsList(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = []

    def get(self, request, *args, **kwargs):
        data = {}
        cats = Category.objects.all()
        for cat in cats:
            data[cat.id] = []
            for product in Product.objects.filter(category_id=cat.id):
                data[cat.name].append(ProductSerializer(product).data)
        return Response(data)
