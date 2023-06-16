from decimal import Decimal
from rest_framework import serializers
from .models import Product, Collection


# class CollectionSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     title = serializers.CharField(max_length=255)


class CollectionSerializer(serializers.Serializer):
    class Meta:
        model = Collection
        fields = ['id', 'title']


# class ProductSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     title = serializers.CharField(max_length=255)
#     price = serializers.DecimalField(max_digits=6, decimal_places=2, source='unit_price')
#     price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')
#     collection = serializers.HyperlinkedRelatedField(
#         queryset=Collection.objects.all(),
#         view_name='collection-detail'
#     )

#     def calculate_tax(self, product: Product):
#         return product.unit_price * Decimal(1.1)

class ProductSerializer(serializers.ModelSerializer):
    # price = serializers.DecimalField(max_digits=6, decimal_places=2, source='unit_price')
    price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')
    # collection = serializers.HyperlinkedRelatedField(
    #     queryset=Collection.objects.all(),
    #     view_name='collection-detail'
    # )

    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'slug', 'inventory', 'unit_price', 'price_with_tax', 'collection']
        # fields = ['id', 'title', 'price', 'price_with_tax', 'collection']
        # fields = '__all__'

    def calculate_tax(self, product: Product):
        return product.unit_price * Decimal(1.1)

    # Overwriting the validation method
    # def validate(self, data):
    #     if data['password'] != data['confirm_password']:
    #         return serializers.ValidationError('Passwords do not match.')
    #     return data

    # Overwriting the creation method
    # def create(self, validated_data):
    #     product = Product(**validated_data)
    #     product.other = 1
    #     product.save()
    #     return product

    # Overwriting the update method
    # def update(self, instance, validated_data):
    #     instance.unit_price = validated_data['unit_price']
    #     instance.save()
    #     return instance
