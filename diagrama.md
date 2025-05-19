```mermaid
classDiagram
    Cliente "1" o-- "0..*" Pedido : faz
    Pedido "0..*" o-- "0..*" Pizza : contém
    Pizza "0..*" o-- "0..*" Sabor : tem

    class Cliente {
        +id: AutoField
        +nome: CharField(max_length=100)
        +telefone: CharField(max_length=15)
        +endereco: TextField
    }

    class Sabor {
        +id: AutoField
        +nome: CharField(max_length=100) <<unique>>
        +descricao: TextField
    }

    class Pizza {
        +id: AutoField
        +tamanho: CharField(choices=TAMANHOS)
    }

    class Pedido {
        +id: AutoField
        +data_pedido: DateTimeField(auto_now_add=True)
    }
