import streamlit as st
import sqlite3
from datetime import date
import pandas as pd

def create_table():
    conn = sqlite3.connect("dados.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
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

def insert_data(nome, assunto_alerta, tipo_alerta, dt_registro, valor, valores_projecao, produto):
    conn = sqlite3.connect("dados.db")
    cursor = conn.cursor()

    # Verifica se já existe um registro com o mesmo nome e assunto
    cursor.execute("""
        SELECT id FROM users WHERE nome = ? AND assunto_alerta = ? AND tipo_alerta = ?
    """, (nome, assunto_alerta, tipo_alerta))
    existing_record = cursor.fetchone()

    if not existing_record:
        cursor.execute("""
            INSERT INTO users (nome, assunto_alerta, tipo_alerta, dt_registro, valor, valores_projecao, produto) 
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (nome, assunto_alerta, tipo_alerta, dt_registro, valor, valores_projecao, produto))
        conn.commit()

    conn.close()
    
def busca_produto():
    con = sqlite3.connect("fat.db") 
    cursor = con.cursor()
    try:
        # Tentando consultar a tabela de produtos. Substitua conforme necessário.
        cursor.execute("SELECT DISTINCT nome_coluna_outra_tabela FROM outra_tabela")  # Ajuste conforme necessário
        nomes_colunas = [desc[0] for desc in cursor.description]
        dfFat = pd.DataFrame(cursor.fetchall(), columns=nomes_colunas)

        # Verificando se a consulta trouxe dados
        if not dfFat.empty:
            return dfFat['nome_coluna_outra_tabela']  # Ajuste conforme necessário
        else:
            st.error("Nenhum produto encontrado na tabela.")
            return []  # Retorna uma lista vazia se não encontrar dados
    except sqlite3.OperationalError as e:
        st.error(f"Erro ao acessar a tabela de produtos: {e}")
        return []  # Retorna uma lista vazia em caso de erro
    finally:
        cursor.close()
        con.close()

def fetch_data(nome=None):
    conn = sqlite3.connect("dados.db")
    cursor = conn.cursor()
    if nome:
        cursor.execute("SELECT * FROM users WHERE nome = ?", (nome,))
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

def main():
    st.title("Formulário de Cadastro de Alertas")
    
    create_table()
    
    produto = None
    prod = None
    urc = None
    
    nome = st.text_input("Nome")
    dt_registro = date.today().strftime("%d/%m/%Y")    
    
    Ind_Prod = ["","Sim","Não"]
    prod = st.selectbox("O Alerta será por produto?", Ind_Prod)
    
    if prod == "Sim":
        produtos_lista = busca_produto()
        if produtos_lista:  # Verifica se a lista não está vazia
            produto = st.selectbox("Produtos:", sorted(produtos_lista))
        else:
            produto = None  # Se a lista estiver vazia, não exibe a selectbox

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
            insert_data(nome, assunto_alerta, tipo_alerta, dt_registro, valor, valores_projecao, produto)
            st.success("Dados salvos com sucesso!")
        else:
            st.error("Por favor, preencha todos os campos obrigatórios.")

    if st.checkbox("Mostrar dados cadastrados por Nome"):
        names = get_all_names()
        if names:
            name_to_search = st.selectbox("Selecione o nome para buscar os alertas:", sorted(names, key=str.lower))
            if name_to_search:
                data = fetch_data(name_to_search)
                if data:
                    st.write(f"### Alertas para o nome: {name_to_search}")
                    for row in data:
                        st.write(f"**Alerta ID:** {row[0]}")
                        st.write(f"**Assunto:** {row[2]}")
                        if row[3]:  
                            st.write(f"**Tipo de Alerta:** {row[3]}")
                        if row[5]:
                            st.write(f"**Valor a ultrapassar:** R$ {row[5]:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
                        if row[7]:
                            st.write(f"**Campos a Comparar:** {row[2]} e {row[7]}")
                        st.write(f"**Data da Criação:** {row[4]}")
                        if row[8]:
                            st.write(f"**Alerta do Produto:** {row[8]}")
                        else:
                            st.write(f"**Alerta do Produto: TODOS** ")
                        
                else:
                    st.write(f"Nenhum dado encontrado para o nome '{name_to_search}'.")
        else:
            st.write("Nenhum nome cadastrado.")

    if st.checkbox("Mostrar todos os dados cadastrados"):
        data = fetch_data()
        for row in data:
            if row[1] is not None:
                st.write(f"**Alerta ID:** {row[0]}")
                st.write(f"**Nome:** {row[1]}")
                st.write(f"**Assunto:** {row[2]}")
                if row[3]:  
                    st.write(f"**Tipo de Alerta:** {row[3]}")
                if row[5]:
                    st.write(f"**Valor a ultrapassar:** R$ {row[5]:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
                if row[7]:
                    st.write(f"**Campos a Comparar:** {row[2]} e {row[7]}")
                st.write(f"**Data da Criação:** {row[4]}")
                if row[8]:
                    st.write(f"**Alerta do Produto:** {row[8]}")
                else:
                    st.write(f"**Alerta do Produto: TODOS** ") 
                
            else:
                st.write("Nenhum dado cadastrado ainda.")

if __name__ == "__main__":
    main()
