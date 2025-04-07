import streamlit as st
from streamlit_option_menu import option_menu
import sqlite3
import matplotlib.pyplot as plt  # Adicione esta linha para importar o matplotlib
from Formulario_bd3 import insert_data, fetch_data, get_all_names, busca_produto  # Importando funções de Formulario_bd3

st.set_page_config(
    page_title="Sistema de Alertas",
    page_icon="https://www.serpro.gov.br/menu/noticias/noticias-2022/comunicado-aos-empregados-do-serpro/@@images/image/large",
    layout="wide",
    initial_sidebar_state="expanded"
)

def carregar_dados():
    dados = fetch_data()
    return dados

def pagina_home():
    st.title("Dashboard de Alertas")
    dados = carregar_dados()

    if not dados:
        st.warning("Nenhum alerta cadastrado.")
        return

    st.markdown(f"**Total de Alertas:** {len(dados)}")

    assuntos = {}
    for dado in dados:
        assunto = dado[2]
        assuntos[assunto] = assuntos.get(assunto, 0) + 1

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

    st.subheader("Detalhes dos Alertas")
    col1, col2, col3 = st.columns(3)
    cols = [col1, col2, col3]
    for i, dado in enumerate(dados):
        with cols[i % 3]:
            valor_raw = dado[5]
            try:
                valor_formatado = float(str(valor_raw).replace("R$", "").replace(".", "").replace(",", "."))
            except:
                valor_formatado = valor_raw  # fallback se não puder converter

            with st.container(border=True):
                st.markdown(f"**Alerta ID:** {dado[0]}")
                st.markdown(f"**Nome:** {dado[1]}")
                st.markdown(f"**Assunto do Alerta:** {dado[2]}")
                st.markdown(f"**Tipo de Alerta:** {dado[3]}")
                st.markdown(f"**Data de Registro:** {dado[4]}")
                st.markdown(f"**Valor:** R$ {valor_formatado:,.2f}" if isinstance(valor_formatado, float) else f"**Valor:** {valor_formatado}")

def pagina_formulario():
    st.title("Formulário de Cadastro de Alertas")

    nome = st.text_input("Nome")
    dt_registro = st.date_input("Data de Criação")
    
    # Adicionando a lógica do novo formulário
    Ind_Prod = ["", "Sim", "Não"]
    prod = st.selectbox("O Alerta será por produto?", Ind_Prod)
    
    produto = None
    if prod == "Sim":
        produtos_lista = busca_produto()
        produto = st.selectbox("Produtos:", sorted(produtos_lista))
    
    tipo_alerta_options = ["", "Ultrapassar Valor", "Comparar Valores"]
    tipo_alerta = st.selectbox("Tipo de Alerta", tipo_alerta_options)
    
    assunto_alerta = None
    if tipo_alerta != "":
        options = ["", "Faturamento(Valor Bruto)", "Faturamento(Valor Liquido)"]
        assunto_alerta = st.selectbox("Assunto do Alerta", options)
    
    valor = None
    valores_projecao = None
    if tipo_alerta == "Ultrapassar Valor":
        valor = st.number_input("Valor a ultrapassar:")
    elif tipo_alerta == "Comparar Valores":
        valores_projecao = "Projeção"

    if st.button("Enviar"):
        if nome and assunto_alerta:
            insert_data(nome, assunto_alerta, tipo_alerta, dt_registro.strftime("%d/%m/%Y"), valor, valores_projecao, produto)
            st.success("Dados salvos com sucesso!")
        else:
            st.error("Por favor, preencha todos os campos obrigatórios.")

def main():
    with st.sidebar:
        escolha = option_menu(
            "Menu", ["Home", "Criar Alerta"],
            icons=["house", "plus-circle"],
            menu_icon="cast", default_index=0,
            orientation="vertical"
        )

    if escolha == "Home":
        pagina_home()
    elif escolha == "Criar Alerta":
        pagina_formulario()

if __name__ == "__main__":
    main()
