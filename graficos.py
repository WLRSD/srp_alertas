import streamlit as st
import matplotlib.pyplot as plt
from Formulario_bd3 import fetch_data  # Importando a função para pegar os dados

def pagina_graficos():
    st.title("Gráficos de Alertas")
    dados = fetch_data()  # Pega todos os dados dos alertas

    if not dados:
        st.warning("Nenhum alerta cadastrado.")
        return

    st.subheader("Gráfico de Alertas por Tipo de Faturamento")
    
    assuntos = {}
    for dado in dados:
        assunto = dado[2]
        assuntos[assunto] = assuntos.get(assunto, 0) + 1

    # Gráfico de barras
    fig, ax = plt.subplots(figsize=(6, 3))
    cores = []
    legenda_labels = {
        "Faturamento(Valor Bruto)": "Bruto",
        "Faturamento(Valor Liquido)": "Líquido"
    }
    for assunto in assuntos.keys():
        if assunto == "Faturamento(Valor Bruto)":
            cores.append("skyblue")
        else:
            cores.append("salmon")

    ax.bar(assuntos.keys(), assuntos.values(), color=cores)
    ax.set_title("Alertas por Tipo de Faturamento")
    ax.set_ylabel("Quantidade")
    ax.set_xlabel("Assunto")

    for i, (label, valor) in enumerate(assuntos.items()):
        ax.text(i, valor + 0.05, str(valor), ha='center')

    handles = [
        plt.Rectangle((0, 0), 1, 1, color="skyblue", label="Faturamento(Valor Bruto)"),
        plt.Rectangle((0, 0), 1, 1, color="salmon", label="Faturamento(Valor Liquido)")
    ]
    ax.legend(handles=handles)

    st.pyplot(fig)
