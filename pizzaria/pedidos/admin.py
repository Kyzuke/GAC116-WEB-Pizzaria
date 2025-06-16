from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.utils import timezone

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
    extra = 1                      # sempre um form em branco já visível
    fields = ('pizza', 'quantity')
    # nada de readonly_fields, autocomplete_fields nem raw_id_fields
    can_delete = True              # permite excluir itens se quiser
    
# ——— Admin de Order (agora “Pedidos”) ———
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'get_cliente', 
        'get_rua',
        'get_cidade',
        'get_cep',
        'criacao_formatada'
    )
    list_filter = ('created_at'),
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
    
    def get_cliente(self, obj):
        return obj.user.cliente.nome
    get_cliente.short_description = 'Cliente'
    get_cliente.admin_order_field = 'user__cliente__nome'
    
    def criacao_formatada(self, obj):
        data_local = timezone.localtime(obj.created_at)
        return data_local.strftime('%d/%m/%Y %H:%M')
    criacao_formatada.short_description = 'Criado em'
