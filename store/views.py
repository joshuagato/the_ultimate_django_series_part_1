from django.shortcuts import get_object_or_404
from django.db.models.aggregates import Count
from django.http import HttpRequest, HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, UpdateModelMixin
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.decorators import api_view
from rest_framework.permissions import (IsAuthenticated,
                                        AllowAny,
                                        IsAdminUser,
                                        DjangoModelPermissions,
                                        DjangoModelPermissionsOrAnonReadOnly
                                    )
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.request import Request
from rest_framework import status
from .models import Product, Collection, OrderItem, Review, Cart, CartItem, Customer
from .serializers import (
                            ProductSerializer,
                            CollectionSerializer,
                            ReviewSerializer,
                            CartSerializer,
                            CartItemSerializer,
                            AddCartItemSerializer,
                            UpdateCartItemSerializer,
                            CustomerSerializer,
                        )
from .filters import ProductFilter
from .pagination import DefaultPagination
from .permissions import IsAdminOrReadOnly, FullDjangoModelPermissions, ViewCustomerHistoryPermission


class ProductVewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    pagination_class = DefaultPagination
    permission_classes = [IsAdminOrReadOnly]
    search_fields = ['title', 'description']
    ordering_fields = ['unit_price', 'last_update']


    def get_serializer_context(self):
        return {'request': self.request}


    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id=kwargs['pk']).count() > 0:
            return Response({'error': 'Product cannot be deleted because it is associated with an order item.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

        return super().destroy(request, *args, **kwargs)


class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(products_count=Count('products')).all()
    serializer_class = CollectionSerializer
    permission_classes = [IsAdminOrReadOnly]

    def destroy(self, request, *args, **kwargs):
        if Collection.objects.filter(pk=kwargs['pk']).products.count() > 0:
            return Response({'error': 'Collection cannot be deleted because it includes one or more products.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

        return super().destroy(request, *args, **kwargs)


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['product_pk'])

    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_pk']}


class CartViewSet(CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, GenericViewSet):
    queryset = Cart.objects.prefetch_related('items__product').all()  # preload cart-items plus products
    serializer_class = CartSerializer


class CartItemViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerializer
        elif self.request.method == 'PATCH':
            return UpdateCartItemSerializer
        return CartItemSerializer

    def get_serializer_context(self):
        return {'cart_id': self.kwargs['cart_pk']}

    def get_queryset(self):
        return CartItem.objects.filter(cart_id=self.kwargs['cart_pk']).select_related('product')


class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAdminUser]
    # permission_classes = [DjangoModelPermissions]
    # permission_classes = [FullDjangoModelPermissions]
    # permission_classes = [DjangoModelPermissionsOrAnonReadOnly]

    @action(detail=True, permission_classes=[ViewCustomerHistoryPermission])
    def history(self, request, pk):
        return Response('ok')

    @action(detail=False, methods=['GET', 'PUT'], permission_classes=[IsAuthenticated])
    def me(self, request):
        (customer, created) = Customer.objects.get_or_create(user_id=request.user.id)

        if request.method == 'GET':
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = CustomerSerializer(customer, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

# The updated implementation of this viewset is the code block at the top
# class CustomerViewSet(CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
#     queryset = Customer.objects.all()
#     serializer_class = CustomerSerializer
#     permission_classes = [IsAuthenticated,] # This setting applies to all the mixin operations here

#     # Here we set the permissions by return a list of permissions instances instead of permissions classes
#     # def get_permissions(self):
#     #     if self.request.method == 'GET':
#     #         return [AllowAny()]
#     #     return [IsAuthenticated()]

#     # @action(detail=False, methods=['GET', 'PUT'], permission_classes=[IsAuthenticated]) # This operation applies to only this method/action
#     @action(detail=False, methods=['GET', 'PUT'])
#     def me(self, request):
#         (customer, created) = Customer.objects.get_or_create(user_id=request.user.id)

#         if request.method == 'GET':
#             serializer = CustomerSerializer(customer)
#             return Response(serializer.data)
#         elif request.method == 'PUT':
#             serializer = CustomerSerializer(customer, data=request.data)
#             serializer.is_valid(raise_exception=True)
#             serializer.save()
#             return Response(serializer.data)