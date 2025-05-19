# your_app/management/commands/generate_pizzas.py
from django.core.management.base import BaseCommand
from itertools import combinations
from pedidos.models import Sabor, Pizza

class Command(BaseCommand):
    help = "Gera todas as combinações possíveis de Pizza (tamanhos × subsets de sabores)"

    def handle(self, *args, **options):
        tamanhos = ['P', 'M', 'G']
        sab_list = list(Sabor.objects.all())
        criadas = 0

        # Para cada tamanho, para cada subset não-vazio de sabores...
        for r in range(1, len(sab_list) + 1):
            for combo in combinations(sab_list, r):
                for t in tamanhos:
                    # verifica se já existe uma pizza com esse tamanho e exatamente esses sabores
                    qs = Pizza.objects.filter(tamanho=t)
                    if any(set(p.sabores.all()) == set(combo) for p in qs):
                        continue

                    p = Pizza.objects.create(tamanho=t)
                    p.sabores.set(combo)
                    criadas += 1

        self.stdout.write(self.style.SUCCESS(
            f'{criadas} pizzas criadas com sucesso!'))


'''class Command(BaseCommand):
    help = "Gera pizzas de cada tamanho para cada sabor (1 sabor por pizza)"

    def handle(self, *args, **options):
        tamanhos = ['P', 'M', 'G']
        criadas = 0

        for sabor in Sabor.objects.all():
            for t in tamanhos:
                # Verifica se já existe uma pizza desse tamanho com esse sabor
                if not Pizza.objects.filter(tamanho=t, sabores=sabor).exists():
                    p = Pizza.objects.create(tamanho=t)
                    p.sabores.add(sabor)
                    criadas += 1

        self.stdout.write(self.style.SUCCESS(
            f'{criadas} pizzas de 1 sabor criadas com sucesso!'))'''