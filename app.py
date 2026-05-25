import streamlit as st
from finlytics import carregar_extrato, calcular_resumo, top_categorias_gasto, extrair_transacoes_de_pdf

def formatar_moeda(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

st.set_page_config(
    page_title="Finlytics",
    page_icon="💰",
    layout="centered",
)

st.title("💰 Finlytics")
st.write("Assistente Financeiro Pessoal")

arquivo = st.file_uploader("Envie seu extrato (CSV, PDF ou imagem)", type=["csv", "pdf", "png", "jpg", "jpeg"])

if arquivo is None:
    st.info("👆 Envie um arquivo (CSV, PDF ou imagem) para ver a análise")

else:
    if arquivo.name.lower().endswith(".csv"):
        df = carregar_extrato(arquivo)
    else:
        df = extrair_transacoes_de_pdf(arquivo)

    meses_disponiveis = ["Todos"] + list(df["data"].dt.strftime("%Y-%m").unique())
    mes_escolhido = st.selectbox("Mês", meses_disponiveis)
    
    if mes_escolhido == "Todos":
        df_filtrado = df.copy()
    else:
        df_filtrado = df[df["data"].dt.strftime("%Y-%m") == mes_escolhido].copy()
    
    df_filtrado["data"] = df_filtrado["data"].dt.strftime("%d/%m/%Y")


    # Tabela editável (usuário pode corrigir categorias)
    st.subheader("Transações do mês")
    df_editado = st.data_editor(
        df_filtrado,
        disabled=[],
        use_container_width=True,
        column_config={
            "valor": st.column_config.NumberColumn(
                "Valor",
                format="R$ %.2f"
            ),
        },
    )

    # A partir daqui, tudo usa df_editado
    resumo = calcular_resumo(df_editado)

    st.subheader("Resumo do mês")
    col1, col2, col3 = st.columns(3)
    col1.metric("Receitas", formatar_moeda(resumo["total_receitas"]))
    col2.metric("Despesas", formatar_moeda(resumo["total_despesas"]))
    col3.metric("Saldo do mês", formatar_moeda(resumo["saldo"]))

    st.subheader("Top 3 categorias de gasto")
    top3 = top_categorias_gasto(df_editado, n=3)
    st.bar_chart(top3)