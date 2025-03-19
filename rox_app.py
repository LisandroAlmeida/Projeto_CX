import streamlit as st
import pandas as pd
import io
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Configuração da Página
st.set_page_config(page_title="Cálculo de ROX", layout="wide")

st.title("📊 Cálculo de ROX - Retorno sobre a Experiência")

# Seção 1: Ação de CX
st.header("1️⃣ Ação de CX")

col1, col2 = st.columns(2)
with col1:
    nome_iniciativa = st.text_input("Nome da Ação", placeholder=" ")
    produto_servico = st.text_input("Produto/Serviço da Ação", placeholder=" ")
    valor_servico = st.number_input("Valor do Serviço/Produto da Ação (R$)", min_value=0.0, format="%.2f")
    data_inicio = st.date_input("Data de Início")
    data_fim = st.date_input("Data de Término")

    # Formatar as datas corretamente
    data_inicio_formatada = data_inicio.strftime("%d/%m/%Y")
    data_fim_formatada = data_fim.strftime("%d/%m/%Y")

with col2:
    houve_investimento = st.radio("Teve Investimento?", ["Sim", "Não"])
    investimento_total = (
        st.number_input("Valor Investido (R$)", min_value=0.0, format="%.2f") if houve_investimento == "Sim" else 0.0
    )
    repeticao_acao = st.radio("Frequência da Ação?", ["Primeira Ação", "Ação Repetida"])

    if repeticao_acao == "Ação Repetida":
        valor_medio_antes = st.number_input("Valor Médio Gasto por Cliente (Antes) (R$)", min_value=0.0, format="%.2f")

# Seção 2: Números Antes da Ação
st.header("2️⃣ Números Antes da Ação")

col3, col4 = st.columns(2)
with col3:
    clientes_antes = st.number_input("Clientes Atendidos (Antes)", min_value=0)
    recorrentes_antes = st.number_input("Clientes Recorrentes (Antes)", min_value=0)
    indicados_antes = st.number_input("Clientes por Indicação (Antes)", min_value=0)

with col4:
    gasto_adicional_antes = st.radio("Teve clientes com gasto adicional? (Antes)", ["Não", "Sim"])
    if gasto_adicional_antes == "Sim":
        qtd_gasto_antes = st.number_input("Qtd. Clientes com Gasto Adicional (Antes)", min_value=0)
        valor_gasto_antes = st.number_input("Valor Total Gasto Adicional (Antes) (R$)", min_value=0.0, format="%.2f")
    else:
        qtd_gasto_antes, valor_gasto_antes = 0, 0.0

# Cálculos Antes da Ação
total_vendas_antes = clientes_antes * valor_servico
gasto_extra_antes = qtd_gasto_antes * valor_gasto_antes
total_antes = total_vendas_antes + gasto_extra_antes

col_a1, col_a2 = st.columns(2)
col_a1.number_input("💰 Total de Vendas Antes da Ação (R$)", value=total_vendas_antes, format="%.2f", disabled=True)
if gasto_adicional_antes == "Sim":
    col_a2.number_input("➕ Gasto Adicional Antes (R$)", value=gasto_extra_antes, format="%.2f", disabled=True)

# Seção 3: Números Depois da Ação
st.header("3️⃣ Números Depois da Ação")

col5, col6 = st.columns(2)
with col5:
    clientes_depois = st.number_input("Clientes Atendidos (Depois)", min_value=0)
    recorrentes_depois = st.number_input("Clientes Recorrentes (Depois)", min_value=0)
    indicados_depois = st.number_input("Clientes por Indicação (Depois)", min_value=0)

with col6:
    gasto_adicional_depois = st.radio("Teve clientes com gasto adicional? (Depois)", ["Não", "Sim"])
    if gasto_adicional_depois == "Sim":
        qtd_gasto_depois = st.number_input("Qtd. Clientes com Gasto Adicional (Depois)", min_value=0)
        valor_gasto_depois = st.number_input("Valor Total Gasto Adicional (Depois) (R$)", min_value=0.0, format="%.2f")
    else:
        qtd_gasto_depois, valor_gasto_depois = 0, 0.0

# Cálculos Depois da Ação
total_vendas_depois = clientes_depois * valor_servico
gasto_extra_depois = qtd_gasto_depois * valor_gasto_depois
total_depois = total_vendas_depois + gasto_extra_depois

col_b1, col_b2 = st.columns(2)
col_b1.number_input("💰 Total de Vendas Depois da Ação (R$)", value=total_vendas_depois, format="%.2f", disabled=True)
if gasto_adicional_depois == "Sim":
    col_b2.number_input("➕ Gasto Adicional Depois (R$)", value=gasto_extra_depois, format="%.2f", disabled=True)

# Seção 4: Cálculo do ROX
st.header("4️⃣ Cálculo do ROX")

ganho_recorrentes = recorrentes_depois * valor_servico
ganho_indicados = indicados_depois * valor_servico
total_ganhos = ganho_recorrentes + ganho_indicados + gasto_extra_depois

# Evitar valores negativos
rox = ((total_ganhos - investimento_total) / investimento_total) * 100 if investimento_total > 0 else 0
rox = max(rox, 0)

st.subheader("📌 Resultados:")
col7, col8, col9 = st.columns(3)
col7.metric(label="Total de Ganhos Após a Ação (R$)", value=f"{total_ganhos:,.2f}")
col8.metric(label="Investimento Total (R$)", value=f"{investimento_total:,.2f}")
col9.metric(label="ROX Calculado (%)", value=f"{rox:.2f}%")

# Função para gerar PDF com ReportLab
def gerar_pdf(conteudo):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    
    c.drawString(100, 750, "Relatório de ROX")
    c.drawString(100, 730, f"Nome da Ação: {conteudo['nome_iniciativa']}")
    c.drawString(100, 710, f"Produto/Serviço: {conteudo['produto_servico']}")
    c.drawString(100, 690, f"Data Início: {conteudo['data_inicio']}")
    c.drawString(100, 670, f"Data Fim: {conteudo['data_fim']}")
    c.drawString(100, 650, f"Investimento Total: R$ {conteudo['investimento_total']:,.2f}")
    c.drawString(100, 630, f"Total de Ganhos: R$ {conteudo['total_ganhos']:,.2f}")
    c.drawString(100, 610, f"ROX Calculado: {conteudo['rox']:.2f}%")
    
    c.save()
    buffer.seek(0)
    return buffer

if st.button("📥 Baixar PDF"):
    pdf = gerar_pdf({
        "nome_iniciativa": nome_iniciativa, "produto_servico": produto_servico,
        "data_inicio": data_inicio_formatada, "data_fim": data_fim_formatada,
        "investimento_total": investimento_total, "total_ganhos": total_ganhos, "rox": rox
    })
    st.download_button("Baixar Relatório ROX", pdf, "ROX_Calculo.pdf", "application/pdf")
