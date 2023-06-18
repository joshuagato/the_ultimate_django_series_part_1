from django.urls import path, include
from rest_framework.routers import SimpleRouter, DefaultRouter
from rest_framework_nested import routers
from . import views
from .views import ProductVewSet, CollectionViewSet, ReviewViewSet, CartViewSet, CartItemViewSet
# from pprint import pprint

# router = SimpleRouter()
# router = DefaultRouter()
router = routers.DefaultRouter()
router.register('products', ProductVewSet, basename='products')
router.register('collections', CollectionViewSet)
router.register('carts', CartViewSet)

products_router = routers.NestedDefaultRouter(router, 'products', lookup='product')
products_router.register('reviews', ReviewViewSet, basename='product-reviews')

cart_router = routers.NestedDefaultRouter(router, 'carts', lookup='cart')
cart_router.register('items', CartItemViewSet, basename='cart-items')

# pprint(router.urls)

urlpatterns = router.urls + products_router.urls + cart_router.urls

# # We can use this if we have some other explicit routes
# urlpatterns = [
#     path('', include(router.urls)),
#     # path('some_model', include(some_model.urls)),
# ]
