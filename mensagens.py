import streamlit as st
import sqlite3
import requests 

def cadastrar_webhook(nome, url):
    conn = sqlite3.connect("webhooks.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS webhooks (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT, url TEXT)")
    cursor.execute("INSERT INTO webhooks (nome, url) VALUES (?, ?)", (nome, url))
    conn.commit()
    conn.close()

def obter_webhooks():
    conn = sqlite3.connect("webhooks.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome, url FROM webhooks")  
    webhooks = cursor.fetchall()
    conn.close()
    return webhooks

def enviar_mensagem_de_teste(url_webhook):
    mensagem = "Esta é uma mensagem de teste enviada para o webhook!"
    payload = {
        "text": mensagem  
    }
    try:
        response = requests.post(url_webhook, json=payload)
        if response.status_code == 200:
            return "Mensagem de teste enviada com sucesso!"
        else:
            return f"Erro ao enviar mensagem. Status: {response.status_code}, Detalhes: {response.text}"
    except Exception as e:
        return f"Erro ao enviar mensagem: {e}"

def pagina_mensagens():
    st.title("Mensagens - Webhooks")
    
    
    nome_alerta = st.text_input("Dê um nome ao seu alerta")  
    url = st.text_input("Digite a URL do Webhook")
    
    if st.button("Adicionar Webhook"):
        if nome_alerta and url:
            cadastrar_webhook(nome_alerta, url)  
            st.success(f"Webhook '{nome_alerta}' cadastrado com sucesso!")
        else:
            st.error("Por favor, insira um nome e uma URL válidos.")

    
    webhooks = obter_webhooks()
    if webhooks:
        st.subheader("Webhooks Cadastrados")
        for webhook in webhooks:
            webhook_id, nome, url = webhook  
            with st.expander(f"Webhook: {nome}"):  
                st.write(f"**Nome**: {nome}")
                st.write(f"**URL**: {url}")

                
                if st.button(f"Ativar e Enviar mensagem de teste para {nome}", key=f"enviar_{webhook_id}"):
                    resultado = enviar_mensagem_de_teste(url)
                    st.success(resultado) 

    else:
        st.write("Nenhum webhook cadastrado.")
