import streamlit as st
from streamlit_option_menu import option_menu
import sqlite3
import matplotlib.pyplot as plt
from Formulario_bd3 import insert_data, fetch_data, get_all_names, busca_produto, create_table, busca_valores_brutos, busca_valores_liquidos, pagina_formulario
from graficos import pagina_graficos  # Importando a função para gráficos
from pagina_home import pagina_home  # Importando a página home
from mensagens import pagina_mensagens  # Importando a página de mensagens

st.set_page_config(
    page_title="Sistema de Alertas",
    page_icon="https://www.serpro.gov.br/menu/noticias/noticias-2022/comunicado-aos-empregados-do-serpro/@@images/image/large",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Verificar se a tabela existe, se não criar
create_table()  # Chamando a função para garantir que a tabela 'users' exista

def main():
    with st.sidebar:
        escolha = option_menu(
            "Menu", ["Home", "Criar Alerta", "Gráficos", "Mensagens"],
            icons=["house", "plus-circle", "bar-chart", "chat"],
            menu_icon="cast", default_index=0,
            orientation="vertical"
        )

    if escolha == "Home":
        pagina_home()  # Chamando a função do arquivo pagina_home.py
    elif escolha == "Criar Alerta":
        pagina_formulario()  # Já está com a função do formulário correto
    elif escolha == "Gráficos":
        pagina_graficos()  # Chamando a função do arquivo graficos.py
    elif escolha == "Mensagens":
        pagina_mensagens()  # Chamando a função do arquivo mensagens.py

if __name__ == "__main__":
    main()
