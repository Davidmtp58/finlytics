import streamlit as st
from finlytics import carregar_extrato, calcular_resumo, top_categorias_gasto

def formatar_moeda(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

st.set_page_config(
    page_title="Finlytics",
    page_icon="💰",
    layout="centered",
)

st.title("💰 Finlytics")
st.write("Assistente Financeiro Pessoal")

arquivo = st.file_uploader("Envie seu extrato em CSV", type=["csv"])

if arquivo is None:
    st.info("👆 Envie um arquivo CSV para ver a análise")
else:
    df = carregar_extrato(arquivo)
    df["data"] = df["data"].dt.strftime("%d/%m/%Y")

    # Tabela editável (usuário pode corrigir categorias)
    st.subheader("Transações do mês")
    df_editado = st.data_editor(
        df,
        disabled=["data", "descricao", "valor"],
        use_container_width=True,
        column_config={
            "valor": st.column_config.NumberColumn(
                "Valor",
                format="R$ %.2f"
            ),
        },
    )

    resumo = calcular_resumo(df_editado)

    # A partir daqui, tudo usa df_editado
    resumo = calcular_resumo(df_editado)

    st.subheader("Resumo do mês")
    col1, col2, col3 = st.columns(3)
    col1.metric("Receitas", formatar_moeda(resumo["total_receitas"]))
    col2.metric("Despesas", formatar_moeda(resumo["total_despesas"]))
    col3.metric("Saldo do mês", formatar_moeda(resumo["saldo"]))

    st.subheader("Top 3 categorias de gasto")
    top3 = top_categorias_gasto(df_editado, n=3).abs()
    st.bar_chart(top3)