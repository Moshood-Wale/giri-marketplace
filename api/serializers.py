from rest_framework import serializers
from .models import Artisan, Product, Order, OrderItem
from django.contrib.auth import get_user_model


User = get_user_model()
class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'name', 'password', 'password_confirm', 
                 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")
        return value

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("Passwords do not match")
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        validated_data['username'] = validated_data['email'].split('@')[0]
        
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            name=validated_data.get('name', ''),
            password=validated_data['password']
        )
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'name', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')


class ArtisanSerializer(serializers.ModelSerializer):
    product_count = serializers.SerializerMethodField()

    class Meta:
        model = Artisan
        fields = ['id', 'business_name', 'description', 'location', 
                 'created_at', 'updated_at', 'product_count']
        read_only_fields = ['user']

    def get_product_count(self, obj):
        return obj.products.count()


class ProductSerializer(serializers.ModelSerializer):
    artisan_name = serializers.CharField(source='artisan.business_name', read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'artisan', 'artisan_name', 'name', 'description', 
                 'price', 'inventory', 'image', 'created_at', 'updated_at']
        
    def validate_inventory(self, value):
        if value < 0:
            raise serializers.ValidationError("Inventory cannot be negative")
        return value


class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_name', 'quantity', 'price']

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than zero")
        return value


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'username', 'status', 'total_amount',
                 'items', 'created_at', 'updated_at']
        read_only_fields = ['user']

    def validate(self, data):
        if 'items' in data:
            total = sum(item['quantity'] * item['price'] for item in data['items'])
            if data['total_amount'] != total:
                raise serializers.ValidationError(
                    "Total amount does not match sum of items")
        return data

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        # Create order with user from context
        order = Order.objects.create(
            user=self.context['request'].user,
            **validated_data
        )
        
        for item_data in items_data:
            product = item_data['product']
            quantity = item_data['quantity']
            
            if product.inventory < quantity:
                raise serializers.ValidationError(
                    f"Not enough inventory for product {product.name}")
            
            product.inventory -= quantity
            product.save()
            
            OrderItem.objects.create(order=order, **item_data)
        
        return order