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

# === LGPD: Termo de consentimento ===
if not st.session_state.get("consentimento_dado", False):
    st.warning("⚠️ Aviso de Privacidade — LGPD")
    
    st.markdown("""
    Este aplicativo processa dados de extrato bancário e **envia arquivos PDF/imagem 
    à API do Google Gemini** para extração e classificação de transações.
    
    **Antes de continuar, leia e confirme:**
    """)
    
    ciente_processamento = st.checkbox(
        "Estou ciente que meus dados serão processados pelo sistema e podem ser enviados ao Google Gemini."
    )
    dados_proprios = st.checkbox(
        "Estou usando apenas dados próprios ou fictícios."
    )
    concordo = st.checkbox(
        "Concordo com o uso conforme descrito acima."
    )
    
    if st.button("Aceitar e continuar"):
        if ciente_processamento and dados_proprios and concordo:
            st.session_state["consentimento_dado"] = True
            st.rerun()
        else:
            st.error("Você precisa marcar as três opções para continuar.")
    
    st.stop()

arquivo = st.file_uploader("Envie seu extrato (CSV, PDF ou imagem)", type=["csv", "pdf", "png", "jpg", "jpeg"])

modo_privacidade = st.toggle(
    "🔒 Modo privacidade (não enviar dados para IA)",
    help="Quando ativado, usa apenas o dicionário local. PDF/imagem não funcionam neste modo."
)

if arquivo is None:
    st.info("👆 Envie um arquivo (CSV, PDF ou imagem) para ver a análise")

else:
    if modo_privacidade and not arquivo.name.lower().endswith(".csv"):
        st.error("⚠️ Modo privacidade ativado: apenas CSV é aceito (PDF e imagem dependem da IA).")
        st.stop()
    
    if arquivo.name.lower().endswith(".csv"):
        df = carregar_extrato(arquivo, usar_ia=not modo_privacidade)
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