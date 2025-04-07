#!/usr/bin/env python
# coding: utf-8

# In[20]:


## Busca registros da tabela criada pelo formulário

import sqlite3
import pandas as pd

# Conectar ao banco de dados
conn = sqlite3.connect("dados.db")
cursor2 = conn.cursor()

# Buscar todos os registros
cursor2.execute("SELECT * FROM users")

nomes_colunas = [desc[0] for desc in cursor2.description]

dados = cursor2.fetchall()  # Lista de tuplas com os dados

dfForm = pd.DataFrame(dados, columns=nomes_colunas)

# Fechar conexão
conn.close()


# In[14]:


## Busca dados de Faturamento (cl_faturamento (cópia local))
con = sqlite3.connect("fat.db")  # Conexão personalizada
cursor = con.cursor()  # Criando o cursor

    # Executar a consulta SQL
cursor.execute("SELECT * FROM cl_faturamento_cp")

    # Obter os nomes das colunas
nomes_colunas = [desc[0] for desc in cursor.description]

    # Criar um DataFrame com os resultados
dfFat = pd.DataFrame(cursor.fetchall(), columns=nomes_colunas)

    # Fechar a conexão
cursor.close()
con.close()


# In[15]:


#Cria Consulta para buscar dados na cl_faturamento_cp
import sqlite3
import pandas as pd

def busca_dados(sql):
    # Conectar ao banco de dados usando handler_dl
    con = sqlite3.connect("fat.db")  # Conexão personalizada
    cursor = con.cursor()  # Criando o cursor

    # Executar a consulta SQL
    cursor.execute(sql)

    # Obter os nomes das colunas
    nomes_colunas = [desc[0] for desc in cursor.description]

    # Criar um DataFrame com os resultados
    dfFat2 = pd.DataFrame(cursor.fetchall(), columns=nomes_colunas)

    # Fechar a conexão
    cursor.close()
    con.close()

    return dfFat2  # Retornar o DataFrame


# In[16]:


# Função que cria consulta a ser feita no banco
def roda_consulta(assunto_alerta, tipo_alerta, valor, dt_alerta):
    if not dt_alerta:  # Verifica se 'dt_alerta' está vazio ou None
        if assunto_alerta == "Faturamento(Valor Bruto)":
            sql_query = "SELECT sum(vl_bruto) as total FROM cl_faturamento_cp WHERE cd_ano=2025"
        elif assunto_alerta == "Faturamento(Valor Liquido)":  # Correção: 'elif' no lugar de 'else if'
            sql_query = "SELECT sum(vl_liquido) as total FROM cl_faturamento_cp WHERE cd_ano=2025"
        else:
            return None # Retorna None se não houver um caso correspondente

        return busca_dados(sql_query)
    else:
        return pd.DataFrame({"total": [0]})


# In[17]:


#Armazena os resultados das consultas em um dataframe
resultados = []  # Lista para armazenar os resultados

for b in range(len(dfForm['assunto_alerta'])):
    assunto_alerta = dfForm['assunto_alerta'][b]
    tipo_alerta = dfForm['tipo_alerta'][b]
    valor = dfForm['valor'][b]
    dt_alerta = dfForm['dt_alerta'][b]
    dados2 = roda_consulta(assunto_alerta, tipo_alerta, valor, dt_alerta) 
    resultados.append(dados2)
# Concatenando todos os resultados em um único DataFrame
df_final = pd.concat(resultados, ignore_index=True)


# In[22]:


from datetime import datetime
import json
import requests
import sqlite3

def update_dt_alerta(alerta_id, nova_data):
    try:
        print(f"Atualizando o alerta {alerta_id} com a data {nova_data} no banco de dados.")
        
        # Verificar se nova_data já é uma string
        if isinstance(nova_data, str):
            # Se for uma string no formato 'YYYY-MM-DD', não precisa do strftime
            data_str = nova_data
        else:
            # Se for um objeto datetime, converta para string
            data_str = nova_data.strftime("%Y-%m-%d")  
        
        conn = sqlite3.connect("dados.db")
        cursor = conn.cursor()

        # Atualizar o banco de dados com a nova data para o alerta específico
        cursor.execute("""UPDATE users SET dt_alerta = ? WHERE id = ?""", (data_str, alerta_id))  
        conn.commit()  # Confirma a transação
        print(f"Data {nova_data} para o alerta {alerta_id} foi gravada com sucesso no banco de dados.")
        
        conn.close()
    except Exception as e:
        print(f"Erro ao atualizar a data no banco de dados: {e}")


# Loop pelos alertas
for a in range(len(dfForm['id'])):
 #   dados_atual = resultados[a]  # 'resultados[a]' é um DataFrame
    
    alerta_id = dfForm['id'].iloc[a]  
    data_envio = dfForm['dt_alerta'].iloc[a]
    tipo = dfForm['tipo_alerta'].iloc[a]

    if data_envio is not None:  # Verifica se 'dt_alerta' já não é None
        print(f"🔔 Alerta {alerta_id} já enviado!")
    else:
        if tipo == "Ultrapassar Valor":  
            total_value = df_final['total'].iloc[a]
            valor_value = dfForm['valor'].iloc[a]

            try:
                total_value = float(total_value)
                valor_value = float(valor_value)
            except ValueError as e:
                print(f"Erro ao converter valores: {e}")
                continue  

            if total_value >= valor_value:
                url = "https://serprogovbr.webhook.office.com/webhookb2/38d7eb6d-1279-46db-9e52-043082bef9dd@c2db1c4d-29e6-4330-85e3-fb54b7696668/IncomingWebhook/d0679d342230410ebd84d212d5deb799/ab7201cc-0b6c-4366-ae7d-b30e8b6c6109/V2g-zWukFGRVkqO_OCu_q336WJisMk87zql4sGmPEQ5_E1"

                valor_monetario = f"R$ {valor_value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
                total_monetario = f"R$ {total_value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

                msg = {
                    "text": f"Mensagem enviada via Python após verificação ({dfForm['tipo_alerta'].values[a]}): O valor do faturamento {dfForm['assunto_alerta'].str[18:-1][a]} de {dfFat['cd_ano'].values[a]} ultrapassou o valor de {valor_monetario}, hoje está em {total_monetario}"
                }

                headers = {"Content-Type": "application/json"}
                response = requests.post(url, headers=headers, data=json.dumps(msg))

                if response.status_code == 200:
                    print(f"✅ Mensagem enviada com sucesso para o alerta {alerta_id}!")
                    dt_alerta = datetime.today().date()
                    dt_alerta_texto = dt_alerta.strftime("%Y-%m-%d")
                    update_dt_alerta(a+1, dt_alerta_texto)  # Salva no banco de dados
                    dfForm.at[a, 'dt_alerta'] = dt_alerta  # Atualiza o valor no DataFrame

                else:
                    print(f"❌ Erro ao enviar mensagem: {response.status_code}, {response.text}")
            else:
                print(f"⚠️ Não atingiu a condição para o alerta {alerta_id}.")


# In[23]:


dfForm


# In[ ]:




