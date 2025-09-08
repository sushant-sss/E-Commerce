from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ItemViewSet, RegisterView, CartAPIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register('items', ItemViewSet, basename='items')

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='register'),
    path('cart/', CartAPIView.as_view(), name='cart'),
    path('', include(router.urls)),
]
