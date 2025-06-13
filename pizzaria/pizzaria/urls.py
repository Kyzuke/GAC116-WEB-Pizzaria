# GAC116-WEB-Pizzaria/pizzaria/urls.py

from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    # Django admin
    path('admin/', admin.site.urls),

    # monta tudo que está em pedidos/api/urls.py sob o prefixo /api/
    # portanto teremos:
    #  - POST /api/auth/login/
    #  - POST /api/auth/logout/
    #  - GET  /api/pizzas/
    #  - POST /api/orders/
    path('api/', include('pedidos.api.urls')),

    # front-end estático (HTML + JS puros)
    path('',         TemplateView.as_view(template_name='cliente/login.html'),    name='login'),
    path('register/', TemplateView.as_view(template_name='cliente/register.html'), name='register'),
    path('pizzas/',  TemplateView.as_view(template_name='cliente/pizzas.html'),   name='cardapio'),
    path('checkout/',TemplateView.as_view(template_name='cliente/checkout.html'), name='checkout'),
]
