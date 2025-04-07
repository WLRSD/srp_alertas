import sqlite3

def buscar_alertas():
    conn = sqlite3.connect("dados.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users")
    dados = cursor.fetchall()  # Lista de tuplas com os dados

    conn.close()

    consulta = []
    for row in dados:
        user_id = row[0]
        nome = row[1]
        assunto = row[2]
        tipo_alerta = row[3]
        dt_registro = row[4]
        valor = row[5]

        consulta.append({"id": user_id, "nome": nome, "alerta": tipo_alerta, "registro": dt_registro, "valor": valor})

    return consulta  
