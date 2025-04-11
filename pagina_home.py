import streamlit as st
from streamlit_option_menu import option_menu
import sqlite3
from Formulario_bd3 import fetch_data, create_table  # Importando as funções necessárias

# Função para carregar os dados dos alertas
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

    # Gerando o texto dinâmico com base nos alertas
    valor_acima = sum(1 for dado in dados if dado[3] == "Valor acima")
    valor_abaixo = sum(1 for dado in dados if dado[3] == "Valor abaixo")

    tipos_de_alerta = {dado[2] for dado in dados}  # Obter os diferentes tipos de assunto
    tipos_texto = ", ".join(tipos_de_alerta)

    descricao = f"""
        O dashboard exibe os alertas cadastrados no sistema. 
        Existem **{valor_acima} alertas** do tipo "Valor acima" e **{valor_abaixo} alertas** do tipo "Valor abaixo". 
        Os alertas abrangem os seguintes tipos de assunto: **{tipos_texto}**.
        Abaixo estão os detalhes dos alertas registrados no sistema.
    """
    
    st.markdown(descricao)

    # Linha para separar o texto dos alertas
    st.markdown("---")

    # Detalhes dos alertas
    st.subheader("Detalhes dos Alertas")
    col1, col2, col3 = st.columns(3)
    cols = [col1, col2, col3]

    for i, dado in enumerate(dados):
        with cols[i % 3]:
            valor_raw = dado[5]
            try:
                valor_formatado = float(str(valor_raw).replace("R$", "").replace(".", "").replace(",", "."))
            except:
                valor_formatado = valor_raw  

            
            with st.container():
                st.markdown(f"""
                    <div style="border: 2px solid #444; padding: 10px; border-radius: 5px; background-color: #2E2E2E; margin-bottom: 20px;">
                        <strong>Alerta ID:</strong> {dado[0]}<br>
                        <strong>Nome:</strong> {dado[1]}<br>
                        <strong>Assunto do Alerta:</strong> {dado[2]}<br>
                        <strong>Tipo de Alerta:</strong> {dado[3]}<br>
                        <strong>Data de Registro:</strong> {dado[4]}<br>
                        <strong>Valor:</strong> {valor_formatado if isinstance(valor_formatado, float) else valor_formatado}
                    </div>
                """, unsafe_allow_html=True)

def pagina_formulario():
    st.title("Formulário de Cadastro de Alertas")

    nome = st.text_input("Nome")
    dt_registro = st.date_input("Data de Criação")
    
    
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
            
            insert_data(assunto_alerta, tipo_alerta, dt_registro.strftime("%d/%m/%Y"), valor, valores_projecao if valores_projecao else "", produto)
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
