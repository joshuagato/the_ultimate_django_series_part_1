from django.urls import path, include
from rest_framework.routers import SimpleRouter, DefaultRouter
from rest_framework_nested import routers
from . import views
from .views import (ProductVewSet,
                    ProductImageViewSet,
                    CollectionViewSet,
                    ReviewViewSet,
                    CartViewSet,
                    CartItemViewSet,
                    CustomerViewSet,
                    OrderViewSet
                )

router = routers.DefaultRouter()
router.register('products', ProductVewSet, basename='products')
router.register('collections', CollectionViewSet)
router.register('carts', CartViewSet)
router.register('customers', CustomerViewSet)
router.register('orders', OrderViewSet, basename='orders')

products_router = routers.NestedDefaultRouter(router, 'products', lookup='product')
products_router.register('reviews', ReviewViewSet, basename='product-reviews')
products_router.register('images', ProductImageViewSet, basename='product-images')

cart_router = routers.NestedDefaultRouter(router, 'carts', lookup='cart')
cart_router.register('items', CartItemViewSet, basename='cart-items')

urlpatterns = router.urls + products_router.urls + cart_router.urls
