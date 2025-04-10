import streamlit as st
import sqlite3

def cadastrar_webhook(url):
    conn = sqlite3.connect("webhooks.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS webhooks (id INTEGER PRIMARY KEY AUTOINCREMENT, url TEXT)")
    cursor.execute("INSERT INTO webhooks (url) VALUES (?)", (url,))
    conn.commit()
    conn.close()

def obter_webhooks():
    conn = sqlite3.connect("webhooks.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM webhooks")
    webhooks = cursor.fetchall()
    conn.close()
    return webhooks

def pagina_mensagens():
    st.title("Mensagens - Webhooks")
    
    # Formulário para adicionar webhook
    url = st.text_input("Digite a URL do Webhook")
    if st.button("Adicionar Webhook"):
        if url:
            cadastrar_webhook(url)
            st.success(f"Webhook '{url}' cadastrado com sucesso!")
        else:
            st.error("Por favor, insira uma URL válida.")

    # Exibir todos os webhooks cadastrados
    webhooks = obter_webhooks()
    if webhooks:
        st.subheader("Webhooks Cadastrados")
        for webhook in webhooks:
            with st.expander(f"Webhook {webhook[0]}: {webhook[1]}"):
                # Mostrar os webhooks existentes com as URLs associadas
                st.write(f"**URL**: {webhook[1]}")
                
                # A lógica de envio de mensagens seria colocada aqui se necessário.
                if st.button(f"Ativar e Enviar para Webhook {webhook[0]}", key=webhook[0]):
                    st.write("Mensagem enviada para o webhook!")
                    # Aqui você pode fazer a integração real para enviar a mensagem via webhook.
    else:
        st.write("Nenhum webhook cadastrado.")
