classDiagram
    Cliente "1" o-- "0..*" Pedido : faz
    Pedido "0..*" o-- "0..*" Pizza : contém
    Pizza "0..*" o-- "0..*" Sabor : tem

    class Cliente {
        +int id
        +CharField nome
        +CharField telefone
        +TextField endereco
    }

    class Pedido {
        +int id
        +ForeignKey cliente
        +DateTimeField data_pedido
    }

    class Pizza {
        +int id
        +CharField tamanho
    }

    class Sabor {
        +int id
        +CharField nome
        +TextField descricao
    }
