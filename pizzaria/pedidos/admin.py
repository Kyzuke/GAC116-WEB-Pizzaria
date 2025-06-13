from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import ModelForm

from .models import (
    Cliente,
    Sabor,
    Pizza,
    Order,
    OrderItem,
)

# ——— Cliente ———
@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display  = ('nome', 'telefone', 'endereco')
    search_fields = ('nome', 'telefone')


# ——— Sabor ———
@admin.register(Sabor)
class SaborAdmin(admin.ModelAdmin):
    list_display  = ('nome', 'descricao')
    search_fields = ('nome',)


# ——— Pizza (mantém sua validação customizada) ———
class PizzaForm(ModelForm):
    def clean(self):
        data     = super().clean()
        tamanho  = data.get('tamanho')
        sabores  = data.get('sabores')
        if tamanho and sabores:
            sel = set(sabores.values_list('id', flat=True))
            qs  = Pizza.objects.exclude(pk=self.instance.pk).filter(tamanho=tamanho)
            for p in qs:
                if set(p.sabores.values_list('id', flat=True)) == sel:
                    raise ValidationError(
                        "Já existe uma pizza com essa combinação de tamanho e sabores."
                    )
        return data

@admin.register(Pizza)
class PizzaAdmin(admin.ModelAdmin):
    form = PizzaForm
    filter_horizontal = ('sabores',)


# ——— “Renomeia” Order para aparecer como “Pedido(s)” ———
Order._meta.verbose_name        = 'Pedido'
Order._meta.verbose_name_plural = 'Pedidos'


# ——— Inline de itens de cada pedido ———
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('pizza', 'quantity')


# ——— Admin de Order (agora “Pedidos”) ———
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'get_rua',
        'get_cidade',
        'get_cep',
        'created_at'
    )
    list_filter = ('created_at',)
    inlines    = [OrderItemInline]

    def get_rua(self, obj):
        return obj.address.street
    get_rua.short_description = 'Rua'

    def get_cidade(self, obj):
        return obj.address.city
    get_cidade.short_description = 'Cidade'

    def get_cep(self, obj):
        return obj.address.zip_code
    get_cep.short_description = 'CEP'
