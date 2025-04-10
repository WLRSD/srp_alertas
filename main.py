import streamlit as st
from streamlit_option_menu import option_menu
from Formulario_bd3 import insert_data, fetch_data, get_all_names, busca_produto, create_table, busca_valores_brutos, busca_valores_liquidos
from graficos import pagina_graficos  # Importando a função para gráficos
import matplotlib.pyplot as plt  # Adicionando a importação do matplotlib
from mensagens import pagina_mensagens  # Importando a página de mensagens

st.set_page_config(
    page_title="Sistema de Alertas",
    page_icon="https://www.serpro.gov.br/menu/noticias/noticias-2022/comunicado-aos-empregados-do-serpro/@@images/image/large",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Verificar se a tabela existe, se não criar
create_table()  # Chamando a função para garantir que a tabela 'users' exista

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

    st.write("**Detalhes dos Alertas**")
    for assunto, quantidade in assuntos.items():
        st.write(f"- **{assunto}:** {quantidade} alertas")

    # Remover gráfico da Home
    st.write("Página de Alertas com detalhes dos tipos de alerta.")

def pagina_formulario():
    st.title("Formulário de Cadastro de Alertas")

    nome = st.text_input("Nome")
    dt_registro = st.date_input("Data de Criação")
    
    # Adicionando a lógica do novo formulário
    Ind_Prod = ["", "Sim", "Não"]
    prod = st.selectbox("O Alerta será por produto?", Ind_Prod)
    
    produto = None
    if prod == "Sim":
        produtos_lista = ["Hospedagem de Aplicações","Desenvolvimento e Manutenção de Software","Serpro MultiCloud","Atendimento a Ambientes de Rede Local","Gestão de Margem Consignável","Emplaca - Sistema Nacional de Emplacamento","Datavalid","Consulta Online Senatran","Consulta CPF","Radar - Sistema de Gestão de Infrações de Trânsito"]
        produto = st.selectbox("Produtos:", sorted(produtos_lista))
    
    tipo_alerta_options = ["", "Valor acima", "Valor abaixo"]
    tipo_alerta = st.selectbox("Tipo de Alerta", tipo_alerta_options)
    
    assunto_alerta = None
    if tipo_alerta != "":
        options = ["", "Faturamento(Valor Bruto)", "Faturamento(Valor Liquido)"]
        assunto_alerta = st.selectbox("Assunto do Alerta", options)
    
    valor = None
    valores_projecao = None
    if assunto_alerta == "Faturamento(Valor Liquido)":
        valor_formatado = f"R$ {busca_valores_liquidos(produto):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        st.write(f"Valor atual: {valor_formatado}")
    elif assunto_alerta == "Faturamento(Valor Bruto)":
        valor_formatado = f"R$ {busca_valores_brutos(produto):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        st.write(f"Valor atual: {valor_formatado}")
    
    if tipo_alerta == "Valor acima":
        valor = st.number_input("Valor a comparar:")
    elif tipo_alerta == "Valor abaixo":
        valor = st.number_input("Valor a comparar:")

    if st.button("Enviar"):
        if nome and assunto_alerta:
            # Ajuste: Garantir que valores_projecao seja uma string vazia caso não tenha valor
            insert_data(assunto_alerta, tipo_alerta, dt_registro.strftime("%d/%m/%Y"), valor, valores_projecao if valores_projecao else "", produto)
            st.success("Dados salvos com sucesso!")
        else:
            st.error("Por favor, preencha todos os campos obrigatórios.")

def main():
    with st.sidebar:
        escolha = option_menu(
            "Menu", ["Home", "Criar Alerta", "Gráficos", "Mensagens"],
            icons=["house", "plus-circle", "bar-chart", "chat"],
            menu_icon="cast", default_index=0,
            orientation="vertical"
        )

    if escolha == "Home":
        pagina_home()
    elif escolha == "Criar Alerta":
        pagina_formulario()
    elif escolha == "Gráficos":
        pagina_graficos()  # Chamando a função do arquivo graficos.py
    elif escolha == "Mensagens":
        pagina_mensagens()  # Chamando a função do arquivo mensagens.py

if __name__ == "__main__":
    main()
