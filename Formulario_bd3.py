import streamlit as st
import sqlite3
from datetime import date
import pandas as pd

def check_table_exists():
    conn = sqlite3.connect("dados.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users';")
    result = cursor.fetchone()
    conn.close()
    return result is not None

def create_table():
    # Verificar se a tabela já existe antes de tentar criá-la
    if not check_table_exists():
        conn = sqlite3.connect("dados.db")
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                assunto_alerta TEXT,
                tipo_alerta TEXT,
                dt_registro DATE,
                valor DOUBLE,
                dt_alerta DATE,
                valores_projecao TEXT,
                produto TEXT 
            )
        """)
        conn.commit()
        conn.close()
    else:
        print("Tabela 'users' já existe.")

def insert_data(assunto_alerta, tipo_alerta, dt_registro, valor, valores_projecao, produto):
    conn = sqlite3.connect("dados.db")
    cursor = conn.cursor()

    # Verifica se já existe um registro com o mesmo nome e assunto
    cursor.execute("""
        SELECT id FROM users WHERE assunto_alerta = ? AND tipo_alerta = ? AND valor = ? AND produto = ?
    """, (assunto_alerta,tipo_alerta, valor, produto))
    existing_record = cursor.fetchone()

    if not existing_record:
        cursor.execute("""
            INSERT INTO users (assunto_alerta, tipo_alerta, dt_registro, valor, valores_projecao, produto) 
            VALUES (?, ?, ?, ?, ? ,? )
        """, (assunto_alerta, tipo_alerta, dt_registro, valor, valores_projecao, produto))
        conn.commit()

    conn.close()
    
def busca_produto():
    con = sqlite3.connect("fat.db") 
    cursor = con.cursor()
    cursor.execute("SELECT DISTINCT nm_produto_servico as Produto FROM cl_faturamento_cp")
    nomes_colunas = [desc[0] for desc in cursor.description]
    dfFat = pd.DataFrame(cursor.fetchall(), columns=nomes_colunas)
    return(dfFat['Produto'])
    cursor.close()
    con.close()


def fetch_data(prods=None):
    conn = sqlite3.connect("dados.db")
    cursor = conn.cursor()
    if prods:
        cursor.execute("SELECT * FROM users WHERE produto = ?", (prods,))
    else:
        cursor.execute("SELECT * FROM users")
    data = cursor.fetchall()
    conn.close()
    return data

def get_all_names():
    conn = sqlite3.connect("dados.db")
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT nome FROM users")
    names = [row[0] for row in cursor.fetchall()]
    conn.close()
    return [""] + names
    
def get_all_products():
    conn = sqlite3.connect("dados.db")
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT produto FROM users")
    prods = [row[0] for row in cursor.fetchall()]
    conn.close()
    return [""] + prods    
    
def busca_valores_liquidos(produto):
    con = sqlite3.connect("fat.db")
    cursor = con.cursor()
    if produto:
        cursor.execute(f"SELECT sum(vl_liquido) as total FROM cl_faturamento_cp WHERE cd_ano=2025 and nm_produto_servico = '{produto}';")
    else:
        cursor.execute(f"SELECT sum(vl_liquido) as total FROM cl_faturamento_cp WHERE cd_ano=2025")
    valor_liquido = cursor.fetchone()[0]  
    cursor.close()
    con.close()
    return valor_liquido if valor_liquido else 0
    
def busca_valores_brutos(produto):
    con = sqlite3.connect("fat.db")
    cursor = con.cursor()
    if produto:
        cursor.execute(f"SELECT sum(vl_bruto) as total FROM cl_faturamento_cp WHERE cd_ano=2025 and nm_produto_servico = '{produto}';")
    else:
        cursor.execute(f"SELECT sum(vl_bruto) as total FROM cl_faturamento_cp WHERE cd_ano=2025")
    valor_bruto = cursor.fetchone()[0]  
    cursor.close()
    con.close()
    return valor_bruto if valor_bruto else 0 

def main():
    st.title("Formulário de Cadastro de Alertas")
    
    create_table()
    
    produto = None
    prod = None
    urc = None
    
#    nome = st.text_input("Nome")
    dt_registro = date.today().strftime("%d/%m/%Y")    
    
    Ind_Prod = ["","Sim","Não"]
    prod = st.selectbox("O Alerta será por produto?", Ind_Prod)
    
    if prod == "Sim":
#        produtos_lista = busca_produto()
        produtos_lista = ["Hospedagem de Aplicações","Desenvolvimento e Manutenção de Software","Serpro MultiCloud","Atendimento a Ambientes de Rede Local","Gestão de Margem Consignável","Emplaca - Sistema Nacional de Emplacamento","Datavalid","Consulta Online Senatran","Consulta CPF","Radar - Sistema de Gestão de Infrações de Trânsito"]
        produto = st.selectbox("Produtos:", sorted(produtos_lista))

    
    tipo_alerta_options = ["", "Valor acima", "Valor abaixo"]
    tipo_alerta = st.selectbox("Tipo de Alerta", tipo_alerta_options)

    assunto_alerta = None
    if tipo_alerta != "":
        options = ["Faturamento(Valor Bruto)", "Faturamento(Valor Liquido)"]
        assunto_alerta = st.selectbox("Tipo de Faturamento", options)    
        
    if assunto_alerta == "Faturamento(Valor Liquido)":
        valor_formatado = f"R$ {busca_valores_liquidos(produto):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        st.write(f"Valor atual: {valor_formatado}")
    elif assunto_alerta == "Faturamento(Valor Bruto)":
        valor_formatado = f"R$ {busca_valores_brutos(produto):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        st.write(f"Valor atual: {valor_formatado}")
    
    valor = None 
    valores_projecao = None
    if tipo_alerta == "Valor acima":
        valor = st.number_input("Valor a comparar:")
    elif tipo_alerta == "Valor abaixo":
        valor = st.number_input("Valor a comparar:")

    if st.button("Enviar"):
        if assunto_alerta:
            insert_data(assunto_alerta, tipo_alerta, dt_registro, valor, valores_projecao, produto)
            st.success("Dados salvos com sucesso!")
        else:
            st.error("Por favor, preencha todos os campos obrigatórios.")

    if st.checkbox("Mostrar dados cadastrados por Produto"):
        prods = get_all_products()
        if prods:
            prods_to_search = st.selectbox("Selecione o produto para buscar os alertas:", sorted(prods, key=str.lower))
            if prods_to_search:
                data = fetch_data(prods_to_search)
                if data:
                    st.write(f"### Alertas para o produto: {prods_to_search}")
                    for row in data:
                        st.write(f"**Alerta ID:** {row[0]}")
                        st.write(f"**Assunto:** {row[1]}")
                        if row[2]:  
                            st.write(f"**Tipo de Alerta:** {row[2]}")
                        if row[4]:
                            st.write(f"**Valor a ultrapassar:** R$ {row[4]:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
                        if row[6]:
                            st.write(f"**Campos a Comparar:** {row[1]} e {row[6]}")
                        st.write(f"**Data da Criação:** {row[3]}")
                        if row[7]:
                            st.write(f"**Alerta do Produto:** {row[7]}")
                        else:
                            st.write(f"**Alerta do Produto: TODOS** ")
                        
                       
                else:
                    st.write(f"Nenhum dado encontrado para o produto '{prods_to_search}'.")
        else:
            st.write("Nenhum produto cadastrado.")

    if st.checkbox("Mostrar todos os dados cadastrados"):
        data = fetch_data()
        for row in data:
            if row[1] is not None:
                st.write(f"**Alerta ID:** {row[0]}")
#                st.write(f"**Nome:** {row[1]}")
                st.write(f"**Assunto:** {row[1]}")
                if row[2]:  
                    st.write(f"**Tipo de Alerta:** {row[2]}")
                if row[4]:
                    st.write(f"**Valor a ultrapassar:** R$ {row[4]:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
                if row[6]:
                    st.write(f"**Campos a Comparar:** {row[1]} e {row[6]}")
                st.write(f"**Data da Criação:** {row[3]}")
                if row[7]:
                    st.write(f"**Alerta do Produto:** {row[7]}")
                else:
                    st.write(f"**Alerta do Produto: TODOS** ") 
                
            else:
                st.write("Nenhum dado cadastrado ainda.")

if __name__ == "__main__":
    main()
