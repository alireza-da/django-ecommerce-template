from django.urls import path, include
from shop.views import *
urlpatterns = [
    path('pay/', mock_payment),

    path('orders/', OrderListView.as_view(), name='order-list'),
    path('order/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path('order/', OrderCreateView.as_view(), name='order-create'),
    path('order/user/', OrderUserDetailView.as_view(), name='order-user-detail'),

    path('products/', ProductListView.as_view(), name='product'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('product/', ProductCreateView.as_view(), name='product-create'),

    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('category/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
    path('category/', CategoryCreateView.as_view(), name='category-create'),
    path('category-product/<int:category_id>', CategoryItemsList.as_view(), name='category-product-list'),
    path('categories-products/', CategoriesProductsList.as_view(), name='category-product-list'),

    path('product-images/', ProductImageListView.as_view(), name='product-image-list'),
    path('product-images/<int:pk>/', ProductImageDetailView.as_view(), name='product-image-detail'),
    path('product/', ProductCreateView.as_view(), name='product-create'),


    path('coupons/', CouponListView.as_view(), name='coupon-list'),
    path('coupon/<str:code>/', CouponDetailView.as_view(), name='coupon-detail'),
    path('coupon/', CouponCreateView.as_view(), name='coupon-create'),

    path('order-items/', OrderItemListView.as_view(), name='order-item-list'),
    path('order-item/<int:pk>/', OrderItemCreateView.as_view(), name='order-item-create'),
    path('order-item/', OrderItemDetailView.as_view(), name='order-item-detail'),
    path('order-item/user/', OrderItemUserDetailView.as_view(), name='order-item-user-detail'),

    path('payments/', PaymentListView.as_view(), name='payment-list'),
    path('payment/<int:pk>/', PaymentDetailView.as_view(), name='payment-detail'),
    path('payment/', PaymentCreateView.as_view(), name='payment-create'),
    path('fakepay/', MockPayment.as_view(), name='mock-payment'),

    path('transactions/', TransactionListView.as_view(), name='transaction-list'),
    path('transaction/<int:pk>/', TransactionDetailView.as_view(), name='transaction-detail'),
    path('transaction/', TransactionCreateView.as_view(), name='transaction-create'),
    path('transaction/user/', TransactionUserDetailView.as_view(), name='user-transaction-detail')
]
