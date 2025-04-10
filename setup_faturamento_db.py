import sqlite3
import pandas as pd

def criar_tabela_cl_faturamento_cp():
    conn = sqlite3.connect('fat.db')
    cursor = conn.cursor()

    # Criação da tabela se não existir
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cl_faturamento_cp (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nm_produto_servico TEXT,
        vl_bruto DOUBLE,
        vl_liquido DOUBLE,
        cd_ano INTEGER
    )
    """)

    conn.commit()
    conn.close()
    print("✅ Tabela 'cl_faturamento_cp' criada ou já existente.")

def importar_dados_csv(caminho_csv):
    try:
        df = pd.read_csv(caminho_csv)

        # Verifica se colunas obrigatórias existem
        colunas_esperadas = {'nm_produto_servico', 'vl_bruto', 'vl_liquido', 'cd_ano'}
        if not colunas_esperadas.issubset(df.columns):
            raise ValueError(f"O arquivo CSV deve conter as colunas: {colunas_esperadas}")

        conn = sqlite3.connect('fat.db')
        df.to_sql('cl_faturamento_cp', conn, if_exists='append', index=False)
        conn.close()
        print("📥 Dados importados com sucesso para 'cl_faturamento_cp'.")

    except Exception as e:
        print(f"❌ Erro ao importar CSV: {e}")

if __name__ == "__main__":
    criar_tabela_cl_faturamento_cp()

    # Descomente e edite a linha abaixo para importar seu CSV
    # importar_dados_csv("dados_faturamento.csv")
