from rest_framework import serializers
from .models import Artisan, Product, Order, OrderItem


class ArtisanSerializer(serializers.ModelSerializer):
    # Add product count for better information
    product_count = serializers.SerializerMethodField()

    class Meta:
        model = Artisan
        fields = ['id', 'business_name', 'description', 'location', 
                 'created_at', 'updated_at', 'product_count']

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
        fields = ['id', 'user', 'username', 'status', 'total_amount', 
                 'items', 'created_at', 'updated_at']

    def validate(self, data):
        # Validate total amount matches items
        if 'items' in data:
            total = sum(item['quantity'] * item['price'] for item in data['items'])
            if data['total_amount'] != total:
                raise serializers.ValidationError(
                    "Total amount does not match sum of items")
        return data

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        
        for item_data in items_data:
            # Check inventory before creating order item
            product = item_data['product']
            quantity = item_data['quantity']
            
            if product.inventory < quantity:
                raise serializers.ValidationError(
                    f"Not enough inventory for product {product.name}")
            
            # Reduce inventory
            product.inventory -= quantity
            product.save()
            
            OrderItem.objects.create(order=order, **item_data)
        
        return order