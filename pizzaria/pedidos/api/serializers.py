from rest_framework import serializers
from pedidos.models import Sabor, Pizza, Address, OrderItem, Order
from django.contrib.auth.models import User
from pedidos.models import Cliente

class RegisterSerializer(serializers.ModelSerializer):
    nome     = serializers.CharField(write_only=True)
    telefone = serializers.CharField(write_only=True)
    street   = serializers.CharField(write_only=True)
    city     = serializers.CharField(write_only=True)
    zip_code = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model  = User
        fields = [
            'nome', 'telefone',
            'street', 'city', 'zip_code',
            'username', 'password'
        ]

    def create(self, validated_data):
        # extrai os campos
        nome      = validated_data.pop('nome')
        telefone  = validated_data.pop('telefone')
        street    = validated_data.pop('street')
        city      = validated_data.pop('city')
        zip_code  = validated_data.pop('zip_code')
        password  = validated_data.pop('password')
        username  = validated_data.pop('username')

        # 1) cria o User
        user = User.objects.create_user(username=username, password=password)

        # 2) cria o Cliente
        Cliente.objects.create(
            user=user,
            nome=nome,
            telefone=telefone,
            endereco=f"{street}, {city} – CEP {zip_code}"
        )

        # 3) cria o Address (para a API de checkout)
        Address.objects.create(
            user=user,
            street=street,
            city=city,
            zip_code=zip_code
        )

        return user

class SaborSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Sabor
        fields = ['id', 'nome', 'descricao']

class PizzaSerializer(serializers.ModelSerializer):
    sabores = SaborSerializer(many=True, read_only=True)

    class Meta:
        model  = Pizza
        # liste apenas os campos que existem no modelo
        fields = ['id', 'tamanho', 'sabores']

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Address
        fields = ['id', 'street', 'city', 'zip_code']

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model  = OrderItem
        fields = ['pizza', 'quantity']
        
class OrderSerializer(serializers.ModelSerializer):
    # aceita escrever ou o ID de um endereço existente...
    address_id = serializers.IntegerField(write_only=True, required=False)
    # ...ou um objeto nested para criar um novo
    address    = AddressSerializer(write_only=True, required=False)
    items      = OrderItemSerializer(many=True)

    class Meta:
        model  = Order
        fields = ['id', 'created_at', 'address_id', 'address', 'items']

    def validate(self, data):
        if 'address_id' not in data and 'address' not in data:
            raise serializers.ValidationError(
                "Você deve informar address_id ou address."
            )
        return data

    def create(self, validated_data):
        user    = self.context['request'].user
        items   = validated_data.pop('items')
        # decide se usa um existente
        if 'address_id' in validated_data:
            addr = Address.objects.get(
                id=validated_data.pop('address_id'),
                user=user
            )
        else:
            addr_data = validated_data.pop('address')
            addr = Address.objects.create(user=user, **addr_data)

        order = Order.objects.create(user=user, address=addr)
        for it in items:
            OrderItem.objects.create(order=order, **it)
        return order