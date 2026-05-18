"""
Módulo principal do Finlytics.
Contém a lógica de categorização e cálculos do extrato bancário.
"""

import pandas as pd
import os
from dotenv import load_dotenv
import google.generativeai as genai

# === setup, roda uma vez ===
load_dotenv()                                              
chave = os.getenv("GEMINI_API_KEY")                        
genai.configure(api_key=chave)                             
modelo_gemini = genai.GenerativeModel("gemini-2.5-flash")

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
    df["categoria"] = df["descricao"].apply(classificar_transacao)
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

def classificar_com_gemini(descricao):
    prompt = f"""Você é um classificador de transações bancárias brasileiras.
Sua tarefa: dada a descrição de uma transação, retornar a categoria correspondente.

Categorias possíveis (responda APENAS com uma destas, exatamente como escrito):
- Alimentação
- Transporte
- Streaming
- Saúde
- Salário
- Entrada Diversa
- Outros

Regras:
1. Responda APENAS com o nome da categoria, sem aspas, sem pontuação, sem explicação.
2. Use exatamente a grafia da lista.
3. Se não tiver certeza, responda "Outros".

Exemplos:
Descrição: "IFOOD RESTAURANTE"
Categoria: Alimentação

Descrição: "POSTO IPIRANGA"
Categoria: Transporte

Descrição: "DROGARIA SAO JOAO"
Categoria: Saúde

Agora classifique:
Descrição: "{descricao}"
Categoria:"""

    try:
        resposta = modelo_gemini.generate_content(prompt)
        return resposta.text.strip()
    except Exception as erro:
        print(f"Erro ao chamar Gemini: {erro}")
        return "Outros"
    
def classificar_transacao(descricao):
    """Classifica a transação usando regras locais primeiro e Gemini como fallback."""
    categoria_local = descobrir_categoria(descricao)

    if categoria_local != "Outros":
        return categoria_local

    return classificar_com_gemini(descricao)