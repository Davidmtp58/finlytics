"""
Categorias suportadas pelo Finlytics e classificação por regras locais.
Módulo sem dependências externas para poder ser usado tanto pela app
Streamlit quanto pelo relatório de terminal.
"""

CATEGORIAS_MAP = {
    "IFOOD": "Alimentação",
    "SUPERMERCADO": "Alimentação",
    "LANCHONETE": "Alimentação",
    "UBER": "Transporte",
    "POSTO COMBUSTIVEL": "Transporte",
    "NETFLIX": "Streaming",
    "SPOTIFY": "Streaming",
    "AMAZON PRIME": "Streaming",
    "FARMÁCIA": "Saúde",
    "FARMACIA": "Saúde",
    "SALARIO": "Salário",
    "PIX RECEBIDA": "Entrada Diversa",
    "PIX RECEBIDO": "Entrada Diversa",
    "ACADEMIA": "Fitness",
}

CATEGORIAS_VALIDAS = [
    "Alimentação",
    "Transporte",
    "Streaming",
    "Saúde",
    "Fitness",
    "Salário",
    "Entrada Diversa",
    "Outros",
]


def descobrir_categoria(descricao):
    """Retorna a categoria de uma transação com base na descrição."""
    for palavra_chave, categoria in CATEGORIAS_MAP.items():
        if palavra_chave in descricao:
            return categoria
    return "Outros"
