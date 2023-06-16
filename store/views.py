from django.shortcuts import get_object_or_404
from django.http import HttpRequest, HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from .models import Product
from .serializers import ProductSerializer

@api_view(['GET', 'POST'])
def product_list(request: Request):
    if request.method == 'GET':
        query_set = Product.objects.select_related('collection').all()
        serializer = ProductSerializer(query_set, many=True, context={'request': request})
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        print(serializer.validated_data)
            # request.data => { "title": "a", "unit_price": 2, "collection": 2 }
            # print => OrderedDict([('title', 'a'), ('unit_price', Decimal('2.00')), ('collection', <Collection: Grocery>)])
        return Response(serializer.data, status=status.HTTP_201_CREATED)

        # Same as the block at the top
        # serializer = ProductSerializer(data=request.data)
        # if serializer.is_valid():
        #     serializer.validated_data
        #     return Response('Ok')
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def product_detail(request: Request, id):
    product = get_object_or_404(Product, pk=id)

    if request.method == 'GET':
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = ProductSerializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    elif request.method == 'DELETE':
        # if product.orderitem_set.count() > 0: # related_name attribute not set
        if product.orderitems.count() > 0:
            return Response({'error': 'Product cannot be deleted because it is associated with an order item.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view()
def collection_detail(request: Request, pk):
    return Response('ok')
