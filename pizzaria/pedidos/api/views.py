from django.contrib.auth import authenticate, login, logout
from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import RegisterSerializer, PizzaSerializer, OrderSerializer, AddressSerializer
from pedidos.models import Pizza, Address


class RegisterAPI(APIView):
    authentication_classes = []
    permission_classes     = []

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': True}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPI(APIView):
    """
    POST /api/auth/login/
    Só permite login de usuários não-staff.
    """
    authentication_classes = []
    permission_classes     = []

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and not user.is_staff:
            login(request, user)
            return Response({'success': True})
        return Response(
            {'success': False, 'error': 'Credenciais inválidas'},
            status=status.HTTP_401_UNAUTHORIZED
        )


class LogoutAPI(APIView):
    """
    POST /api/auth/logout/
    Encerra a sessão do usuário autenticado.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({'success': True}, status=status.HTTP_204_NO_CONTENT)


class PizzaViewSet(viewsets.ReadOnlyModelViewSet):
    """
    GET /api/pizzas/
    Lista todos os sabores/tamanhos de pizza.
    """
    queryset = Pizza.objects.all()
    serializer_class = PizzaSerializer
    permission_classes = [permissions.AllowAny]


class OrderViewSet(viewsets.ModelViewSet):
    """
    GET/POST /api/orders/
    Cria e lista pedidos do usuário autenticado.
    """
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.request.user.order_set.all()

class AddressViewSet(viewsets.ReadOnlyModelViewSet):
    """
    GET /api/addresses/
    Lista os endereços do usuário autenticado
    """
    serializer_class   = AddressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)
