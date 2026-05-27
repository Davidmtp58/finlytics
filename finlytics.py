"""
Módulo principal do Finlytics.
Contém a lógica de categorização e cálculos do extrato bancário.
"""

import pandas as pd
import os
from dotenv import load_dotenv
import google.generativeai as genai
import streamlit as st
import json

# === setup, roda uma vez ===
load_dotenv()

try:
    chave = st.secrets["GEMINI_API_KEY"]
except Exception:
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
    "FARMÁCIA": "Saúde",
    "FARMACIA": "Saúde",
    "SALARIO": "Salário",
    "PIX RECEBIDA": "Entrada Diversa",
    "PIX RECEBIDO": "Entrada Diversa",
    "ACADEMIA": "Fitness",
}


def descobrir_categoria(descricao):
    """Retorna a categoria de uma transação com base na descrição."""
    for palavra_chave, categoria in categorias_map.items():
        if palavra_chave in descricao:
            return categoria
    return "Outros"


def carregar_extrato(fonte, usar_ia=True):
    df = pd.read_csv(fonte, parse_dates=["data"])
    df["categoria"] = df["descricao"].apply(lambda d: classificar_transacao(d, usar_ia))
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
- Fitness
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
    
def classificar_transacao(descricao, usar_ia=True):
    categoria_local = descobrir_categoria(descricao)

    if categoria_local != "Outros":
        return categoria_local
    if usar_ia:
        return classificar_com_gemini(descricao)
    return "Outros"

def extrair_transacoes_de_pdf(arquivo_pdf):
    """Usa o Gemini para extrair transações de um PDF de extrato bancário."""
    
    prompt = """Extraia TODAS as transações deste extrato bancário.

Retorne APENAS um array JSON válido, sem texto antes ou depois, no formato:
[
  {"data": "AAAA-MM-DD", "descricao": "DESCRICAO DA TRANSACAO", "valor": -123.45}
]

Regras:
1. data no formato AAAA-MM-DD (ano-mes-dia).
2. valor numerico: negativo para despesas/saidas, positivo para receitas/entradas.
3. descricao em letras maiusculas.
4. Retorne SOMENTE o JSON, nada mais."""

    bytes_pdf = arquivo_pdf.read()

    nome = arquivo_pdf.name.lower()
    if nome.endswith(".pdf"):
        mime = "application/pdf"
    elif nome.endswith(".png"):
        mime = "image/png"
    else:
        mime = "image/jpeg"
    
    resposta = modelo_gemini.generate_content([
        prompt,
        {"mime_type": mime, "data": bytes_pdf}
    ])
    
    # Limpa a resposta (remove marcações markdown que o Gemini adiciona)
    texto = resposta.text.strip()
    if texto.startswith("```json"):
        texto = texto[7:]          
    elif texto.startswith("```"):
        texto = texto[3:]          
    if texto.endswith("```"):
        texto = texto[:-3]         
    texto = texto.strip()
    
    # Converte JSON em DataFrame
    dados = json.loads(texto)
    df = pd.DataFrame(dados)
    df["data"] = pd.to_datetime(df["data"])
    df["categoria"] = df["descricao"].apply(classificar_transacao)
    
    return df