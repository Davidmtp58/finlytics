import streamlit as st
import plotly.graph_objects as go   
from finlytics import carregar_extrato, calcular_resumo, top_categorias_gasto, extrair_transacoes_de_pdf

def card_metrica(titulo, valor, cor_borda="#00D47E"):
    return f"""
    <div style="
        background-color: #1A1F2B;
        border-left: 4px solid {cor_borda};
        border-radius: 8px;
        padding: 16px 20px;
        margin: 8px 0;
    ">
        <div style="color: #9CA3AF; font-size: 14px; margin-bottom: 4px;">
            {titulo}
        </div>
        <div style="color: #FAFAFA; font-size: 26px; font-weight: 600;">
            {valor}
        </div>
    </div>
    """

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
    cor_saldo = "#00D47E" if resumo["saldo"] >= 0 else "#EF4444"
    col1.markdown(card_metrica("Receitas", formatar_moeda(resumo["total_receitas"]), "#00D47E"), unsafe_allow_html=True)
    col2.markdown(card_metrica("Despesas", formatar_moeda(resumo["total_despesas"]), "#EF4444"), unsafe_allow_html=True)
    col3.markdown(card_metrica("Saldo do mês", formatar_moeda(resumo["saldo"]), cor_saldo), unsafe_allow_html=True)

    st.subheader("Top 3 categorias de gasto")
    top3 = top_categorias_gasto(df_editado, n=3)
    
    figura = go.Figure(
        data=[go.Bar(
            x=top3.index,
            y=top3.values,
            marker_color="#00D47E",
        )]
    )
    figura.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="#FAFAFA",
        margin=dict(t=10, b=10, l=10, r=10),
    )
    st.plotly_chart(figura, use_container_width=True)