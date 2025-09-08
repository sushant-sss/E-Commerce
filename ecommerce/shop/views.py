from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from .models import Category, Item, Cart, CartItem
from .serializers import (
    CategorySerializer, ItemSerializer, RegisterSerializer,
    CartItemSerializer
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny

# Registration endpoint
class RegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({'msg':'user created'}, status=status.HTTP_201_CREATED)

# Item CRUD with filter support
class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all().order_by('-created_at')
    serializer_class = ItemSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        qs = Item.objects.all().order_by('-created_at')
        q = self.request.query_params.get('q')
        cat = self.request.query_params.get('category')
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        if q:
            qs = qs.filter(title__icontains=q)
        if cat:
            qs = qs.filter(category__slug=cat)
        if min_price:
            try: qs = qs.filter(price__gte=float(min_price))
            except: pass
        if max_price:
            try: qs = qs.filter(price__lte=float(max_price))
            except: pass
        return qs

# Cart endpoints
class CartAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_cart(self, user):
        cart, created = Cart.objects.get_or_create(user=user)
        return cart

    def get(self, request):
        cart = self.get_cart(request.user)
        items = cart.items.select_related('item').all()
        serializer = CartItemSerializer(items, many=True)
        return Response({'items': serializer.data})

    def post(self, request):
        # Add item to cart
        cart = self.get_cart(request.user)
        item_id = request.data.get('item_id')
        qty = int(request.data.get('quantity', 1))
        item = get_object_or_404(Item, pk=item_id)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, item=item)
        if not created:
            cart_item.quantity += qty
        else:
            cart_item.quantity = qty
        cart_item.save()
        return Response({'msg':'added'}, status=201)

    def patch(self, request):
        # update quantity
        cart = self.get_cart(request.user)
        cart_item_id = request.data.get('cart_item_id')
        qty = int(request.data.get('quantity', 1))
        cart_item = get_object_or_404(CartItem, pk=cart_item_id, cart=cart)
        if qty <= 0:
            cart_item.delete()
            return Response({'msg':'removed'})
        cart_item.quantity = qty
        cart_item.save()
        return Response({'msg':'updated'})

    def delete(self, request):
        # remove item: expects cart_item_id
        cart = self.get_cart(request.user)
        cart_item_id = request.query_params.get('cart_item_id')
        if not cart_item_id:
            return Response({'error':'cart_item_id required'}, status=400)
        cart_item = get_object_or_404(CartItem, pk=cart_item_id, cart=cart)
        cart_item.delete()
        return Response({'msg':'removed'})

# Frontend page views (serve templates)
def index(request):
    return render(request, 'shop/listing.html')

def login_page(request):
    return render(request, 'shop/login.html')

def signup_page(request):
    return render(request, 'shop/signup.html')

def cart_page(request):
    return render(request, 'shop/cart.html')

def items_page(request):
    return render(request, 'shop/items.html')
