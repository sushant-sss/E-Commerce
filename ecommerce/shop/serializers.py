from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Category, Item, Cart, CartItem

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','email']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    class Meta:
        model = User
        fields = ['username','email','password']
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password']
        )
        # create empty cart
        Cart.objects.create(user=user)
        return user

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','name','slug']

class ItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True, required=False
    )
    class Meta:
        model = Item
        fields = ['id','title','description','price','category','category_id','image','created_at']

class CartItemSerializer(serializers.ModelSerializer):
    item = ItemSerializer(read_only=True)
    item_id = serializers.PrimaryKeyRelatedField(queryset=Item.objects.all(), source='item', write_only=True)
    class Meta:
        model = CartItem
        fields = ['id','item','item_id','quantity']

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True)
    class Meta:
        model = Cart
        fields = ['id','user','items']
