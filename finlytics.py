"""
Módulo principal do Finlytics.
Contém a lógica de categorização e cálculos do extrato bancário.
"""

import pandas as pd


# Mapa de palavras-chave para categorias
categorias_map = {
    "IFOOD": "Alimentação",
    "SUPERMERCADO": "Alimentação",
    "LANCHONETE": "Alimentação",
    "UBER": "Transporte",
    "POSTO COMBUSTIVEL": "Transporte",
    "NETFLIX": "Streaming",
    "SPOTIFY": "Streaming",
    "AMAZON PRIME": "Streaming",
    "FARMACIA": "Saúde",
    "SALARIO": "Salário",
    "PIX RECEBIDA": "Entrada Diversa",
}


def descobrir_categoria(descricao):
    """Retorna a categoria de uma transação com base na descrição."""
    for palavra_chave, categoria in categorias_map.items():
        if palavra_chave in descricao:
            return categoria
    return "Outros"


def carregar_extrato(fonte):
    """Carrega o CSV e adiciona a coluna de categoria."""
    df = pd.read_csv(fonte, parse_dates=["data"])
    df["categoria"] = df["descricao"].apply(descobrir_categoria)
    return df


def calcular_resumo(df):
    """Calcula saldo, total de receitas e total de despesas."""
    total_despesas = df[df["valor"] < 0]["valor"].sum()
    total_receitas = df[df["valor"] > 0]["valor"].sum()
    saldo = total_receitas + total_despesas
    return {
        "saldo": saldo,
        "total_receitas": total_receitas,
        "total_despesas": total_despesas,
    }


def top_categorias_gasto(df, n=3):
    """Retorna as N categorias com maior valor de gasto."""
    total_por_categoria = df.groupby("categoria")["valor"].sum().round(2)
    despesas = total_por_categoria[total_por_categoria < 0].abs()
    return despesas.sort_values(ascending=False).head(n)