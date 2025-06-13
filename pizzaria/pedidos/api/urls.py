from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LoginAPI, LogoutAPI, RegisterAPI, PizzaViewSet, OrderViewSet, AddressViewSet

router = DefaultRouter()
router.register('addresses', AddressViewSet, basename='address')
router.register('pizzas', PizzaViewSet, basename='pizza')
router.register('orders', OrderViewSet, basename='order')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/register/', RegisterAPI.as_view(), name='api-register'),
    path('auth/login/',    LoginAPI.as_view(),    name='api-login'),
    path('auth/logout/',   LogoutAPI.as_view(),   name='api-logout'),
]
