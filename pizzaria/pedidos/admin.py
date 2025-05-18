from django.contrib import admin
from .models import Cliente, Sabor, Pizza, Pedido

'''@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'telefone', 'endereco')
    search_fields = ('nome', 'telefone')

@admin.register(Sabor)
class SaborAdmin(admin.ModelAdmin):
    list_display = ('nome', 'descricao')
    search_fields = ('nome',)

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'data_pedido')
    list_filter = ('data_pedido',)
    filter_horizontal = ('pizzas',)'''

@admin.register(Pizza)
class PizzaAdmin(admin.ModelAdmin):
    filter_horizontal = ('sabores',)

admin.site.register(Cliente)
admin.site.register(Sabor)
admin.site.register(Pedido)