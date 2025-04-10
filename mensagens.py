import streamlit as st
import sqlite3
import requests  # Para enviar a mensagem via webhook

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
    cursor.execute("SELECT id, nome, url FROM webhooks")  # Corrigido para retornar 3 valores
    webhooks = cursor.fetchall()
    conn.close()
    return webhooks

def enviar_mensagem_de_teste(url_webhook):
    mensagem = "Esta é uma mensagem de teste enviada para o webhook!"
    payload = {
        "text": mensagem  # Modificado para usar a chave "text" conforme esperado pelo webhook
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
    
    # Formulário para adicionar webhook
    nome_alerta = st.text_input("Dê um nome ao seu alerta")  # Novo campo para nome do webhook
    url = st.text_input("Digite a URL do Webhook")
    
    if st.button("Adicionar Webhook"):
        if nome_alerta and url:
            cadastrar_webhook(nome_alerta, url)  # Passando nome_alerta como primeiro argumento
            st.success(f"Webhook '{nome_alerta}' cadastrado com sucesso!")
        else:
            st.error("Por favor, insira um nome e uma URL válidos.")

    # Exibir todos os webhooks cadastrados
    webhooks = obter_webhooks()
    if webhooks:
        st.subheader("Webhooks Cadastrados")
        for webhook in webhooks:
            webhook_id, nome, url = webhook  # Desempacotando corretamente a tupla (id, nome, url)
            with st.expander(f"Webhook: {nome}"):  # Exibindo o nome ao invés de "Webhook 1", "Webhook 2", etc.
                st.write(f"**Nome**: {nome}")
                st.write(f"**URL**: {url}")

                # Enviar mensagem de teste
                if st.button(f"Ativar e Enviar mensagem de teste para {nome}", key=f"enviar_{webhook_id}"):
                    resultado = enviar_mensagem_de_teste(url)
                    st.success(resultado)  # Exibe o resultado do envio da mensagem

    else:
        st.write("Nenhum webhook cadastrado.")
