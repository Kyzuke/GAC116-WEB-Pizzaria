from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from .models import Cliente, Sabor, Pizza, Pedido

'''@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'telefone', 'endereco')
    search_fields = ('nome', 'telefone')

@admin.register(Sabor)
class SaborAdmin(admin.ModelAdmin):
    list_display = ('nome', 'descricao')
    search_fields = ('nome',)'''

class PizzaForm(ModelForm):
    def clean(self):
        cleaned_data = super().clean()
        tamanho = cleaned_data.get('tamanho')
        sabores = cleaned_data.get('sabores')

        if tamanho and sabores:
            sabores_ids = set(sabores.values_list('id', flat=True))
            for pizza in Pizza.objects.exclude(id=self.instance.id).filter(tamanho=tamanho):
                if set(pizza.sabores.values_list('id', flat=True)) == sabores_ids:
                    raise ValidationError("Já existe uma pizza com essa combinação de tamanho e sabores.")

        return cleaned_data
    
@admin.register(Pizza)
class PizzaAdmin(admin.ModelAdmin):
    filter_horizontal = ('sabores',)
    form = PizzaForm

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'data_pedido')
    list_filter = ('data_pedido',)
    filter_horizontal = ('pizzas',)


admin.site.register(Cliente)
admin.site.register(Sabor)