from django.conf import settings
from django.db import models

class Address(models.Model):
    user     = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    street   = models.CharField(max_length=255)
    city     = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)

class Order(models.Model):
    user       = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    address    = models.ForeignKey(Address, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)

class OrderItem(models.Model):
    order    = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    pizza    = models.ForeignKey('pedidos.Pizza', on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)

class Cliente(models.Model):
    user     = models.OneToOneField(
                 settings.AUTH_USER_MODEL,
                 on_delete=models.CASCADE,
                 related_name='cliente',
                 null=True,
                 blank=True
               )
    nome     = models.CharField(max_length=100)
    telefone = models.CharField(max_length=15)
    endereco = models.TextField()

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name_plural = "Clientes"

class Sabor(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    descricao = models.TextField(blank=True)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name_plural = "Sabores"

    def delete(self, *args, **kwargs):
        pizzas = list(self.pizza_set.all())
        for pizza in pizzas:
            pizza.delete()
        super().delete(*args, **kwargs)


class Pizza(models.Model):
    TAMANHOS = (
        ('P', 'Pequena'),
        ('M', 'Média'),
        ('G', 'Grande'),
    )
    tamanho = models.CharField(max_length=1, choices=TAMANHOS)
    sabores = models.ManyToManyField(Sabor)

    def __str__(self):
        lista = ', '.join(s.nome for s in self.sabores.all())
        return f"Pizza {self.get_tamanho_display()} de {lista}"

    def delete(self, *args, **kwargs):
        for pedido in self.pedido_set.all():
            pedido.delete()
        super().delete(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Pizzas"

class Pedido(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    pizzas = models.ManyToManyField(Pizza)
    data_pedido = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pedido #{self.id} - {self.cliente.nome}"

    class Meta:
        verbose_name_plural = "Pedidos"
