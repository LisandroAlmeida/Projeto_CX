import streamlit as st
import pandas as pd
import io
import pdfkit

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
    qtd_gasto_antes = st.number_input("Qtd. Clientes com Gasto Adicional (Antes)", min_value=0) if gasto_adicional_antes == "Sim" else 0
    valor_gasto_antes = st.number_input("Valor Total Gasto Adicional (Antes) (R$)", min_value=0.0, format="%.2f") if gasto_adicional_antes == "Sim" else 0.0

# Cálculo bloqueado
total_vendas_antes = (clientes_antes * valor_servico) + valor_gasto_antes
st.number_input("💰 Total de Vendas Antes da Ação (R$)", value=total_vendas_antes, format="%.2f", disabled=True)

# Seção 3: Números Depois da Ação
st.header("3️⃣ Números Depois da Ação")

col5, col6 = st.columns(2)
with col5:
    clientes_depois = st.number_input("Clientes Atendidos (Depois)", min_value=0)
    recorrentes_depois = st.number_input("Clientes Recorrentes (Depois)", min_value=0)
    indicados_depois = st.number_input("Clientes por Indicação (Depois)", min_value=0)

with col6:
    gasto_adicional_depois = st.radio("Teve clientes com gasto adicional? (Depois)", ["Não", "Sim"])
    qtd_gasto_depois = st.number_input("Qtd. Clientes com Gasto Adicional (Depois)", min_value=0) if gasto_adicional_depois == "Sim" else 0
    valor_gasto_depois = st.number_input("Valor Total Gasto Adicional (Depois) (R$)", min_value=0.0, format="%.2f") if gasto_adicional_depois == "Sim" else 0.0

# Cálculo bloqueado
total_vendas_depois = (clientes_depois * valor_servico) + valor_gasto_depois
st.number_input("💰 Total de Vendas Depois da Ação (R$)", value=total_vendas_depois, format="%.2f", disabled=True)

# Seção 4: Cálculo do ROX
st.header("4️⃣ Cálculo do ROX")

ganho_recorrentes = recorrentes_depois * valor_servico
ganho_indicados = indicados_depois * valor_servico
total_ganhos = ganho_recorrentes + ganho_indicados + valor_gasto_depois

# Evitar valores negativos
rox = ((total_ganhos - investimento_total) / investimento_total) * 100 if investimento_total > 0 else 0
rox = max(rox, 0)

st.subheader("📌 Resultados:")
col7, col8, col9 = st.columns(3)
col7.metric(label="Total de Ganhos Após a Ação (R$)", value=f"{total_ganhos:,.2f}")
col8.metric(label="Investimento Total (R$)", value=f"{investimento_total:,.2f}")
col9.metric(label="ROX Calculado (%)", value=f"{rox:.2f}%")

# Exportação de Dados
st.header("📥 Exportar para arquivo:")
export_format = st.radio("", ["PDF", "Excel/Sheets"])

if st.button("Exportar"):
    if export_format == "Excel/Sheets":
        output = io.BytesIO()
        writer = pd.ExcelWriter(output, engine="xlsxwriter")
        df = pd.DataFrame(
            {
                "Nome da Ação": [nome_iniciativa],
                "Produto/Serviço": [produto_servico],
                "Valor Serviço/Produto": [valor_servico],
                "Data Início": [data_inicio],
                "Data Fim": [data_fim],
                "Investimento Total": [investimento_total],
                "Total de Ganhos": [total_ganhos],
                "ROX (%)": [rox],
            }
        )
        df.to_excel(writer, sheet_name="ROX", index=False)
        writer.close()
        output.seek(0)
        st.download_button("📥 Baixar Excel", data=output, file_name="ROX_Calculo.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    elif export_format == "PDF":
        pdf_output = f"""
        <h2>Relatório de ROX</h2>
        <p><strong>Nome da Ação:</strong> {nome_iniciativa}</p>
        <p><strong>Produto/Serviço:</strong> {produto_servico}</p>
        <p><strong>Valor Serviço/Produto:</strong> R$ {valor_servico:,.2f}</p>
        <p><strong>Data Início:</strong> {data_inicio}</p>
        <p><strong>Data Fim:</strong> {data_fim}</p>
        <p><strong>Investimento Total:</strong> R$ {investimento_total:,.2f}</p>
        <p><strong>Total de Ganhos:</strong> R$ {total_ganhos:,.2f}</p>
        <p><strong>ROX Calculado:</strong> {rox:.2f}%</p>
        """

        pdf_path = "relatorio_rox.pdf"
        pdfkit.from_string(pdf_output, pdf_path)
        with open(pdf_path, "rb") as f:
            st.download_button("📥 Baixar PDF", data=f, file_name="ROX_Calculo.pdf", mime="application/pdf")
