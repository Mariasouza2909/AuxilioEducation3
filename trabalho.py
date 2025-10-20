import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
st.title("🏭 Controle de produção de máquinas")

st.write("Gerencie a produção diária e monitore o desempenho de cada máquina da fábrica.")
st.markdown("---")
st.header("Importar ou Criar Base de Dados")

arquivo = st.file_uploader("Selecione um arquivo CSV (ou continue com base existente):", type=["csv"])

if arquivo:
    df = pd.read_csv(arquivo)
    df.to_csv("dados.csv", index=False)
    st.success("✅ Arquivo salvo")
elif os.path.exists("dados.csv"):
    df = pd.read_csv("dados.csv")
else:
    df = pd.DataFrame(columns=["Data", "Máquina", "Turno", "Peças Totais", "Peças com defeito"])
    
st.dataframe(df, use_container_width=True, height=250)
st.markdown("---")
st.header("🧾 Adicionar dados")

col1, col2, col3 = st.columns(3)
with col1:
    data = st.text_input('Data da verificação')
with col2:
    maquina = st.text_input("Máquina")
with col3:
    turno = st.selectbox("Turno", ["", "Manhã", "Tarde", "Noite"])
col4, col5 = st.columns(2)
with col4:
    pecas = st.number_input("Peças Totais", min_value=0)
with col5:
    defeituosas = st.number_input("Peças com defeito", min_value=0)

if st.button("Adicionar registro"):
    if data and maquina and turno:
        novo = pd.DataFrame({
            "Data": [data],
            "Máquina": [maquina],
            "Turno": [turno],
            "Peças Totais": [pecas],
            "Peças com defeito": [defeituosas]
        })

        if os.path.exists("dados.csv"):
            df = pd.read_csv("dados.csv")
            df = pd.concat([df, novo], ignore_index=True)
        else:
            df = novo

        df.to_csv("dados.csv", index=False)
        st.success("✅ Registro adicionado com sucesso!")
        st.dataframe(df.tail(5), use_container_width=True)
    else:
        st.warning("⚠️ Preencha todos os campos obrigatórios (Máquina e Turno).")

st.markdown("---")
st.header("📊 Análises de Produção")

if len(df) == 0:
    st.info("Nenhum dado disponível")
else:
    df["Eficiência (%)"] = ((df["Peças Totais"] - df["Peças com defeito"]) /
                            df["Peças Totais"])

    media = round(df["Eficiência (%)"].mean(), 2)
    total_pecas = df["Peças Totais"].sum()
    total_defeitos = df["Peças com defeito"].sum()

    colM1, colM2, colM3 = st.columns(3)
    colM1.metric("Eficiência", f"{media}%")
    colM2.metric("Peças Produzidas", total_pecas)
    colM3.metric("Defeitos Totais", total_defeitos)

    st.write("Produção por Máquina")
    fig1, ax1 = plt.subplots()
    ax1.bar(df["Máquina"], df["Peças Totais"], color="#3A86FF")
    ax1.set_xlabel("Máquina")
    ax1.set_ylabel("Peças Totais")
    st.pyplot(fig1)

    st.write("Eficiência por Máquina (%)")
    fig2, ax2 = plt.subplots()
    ax2.plot(df["Máquina"], df["Eficiência (%)"], marker="o", color="#FFB703")
    ax2.set_xlabel("Máquina")
    ax2.set_ylabel("Eficiência (%)")
    st.pyplot(fig2)

    alerta = df[(df["Eficiência (%)"] < 90) | (df["Peças Totais"] < 80)]
    if not alerta.empty:
        st.warning("⚠️ Registros com baixa eficiência (<90%) ou baixa produção (<80 peças):")
        
st.markdown("---")
st.header("💾  Exportar Base Atualizada")

nomearq = st.text_input("Nome do arquivo CSV:", "dados.csv")
if st.button("Salvar CSV"):
    df.to_csv(nomearq, index=False)
    st.success(f"Arquivo '{nomearq}' salvo com sucesso!")