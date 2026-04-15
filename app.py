import mysql.connector
from mysql.connector import Error

config = {
    'host': 'localhost',
    'user': 'kadu',       
    'password': '1234',       
    'database': 'sistema_avaliacoes'
}

def conectar():
    try:
        conn = mysql.connector.connect(**config)
        return conn
    except Error as e:
        print(f"Erro ao conectar ao MySQL: {e}")
        return None

def inicializar_banco():
    conn = mysql.connector.connect(host=config['host'], user=config['user'], password=config['password'])
    cursor = conn.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {config['database']}")
    cursor.execute(f"USE {config['database']}")
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS avaliacoes (
            id INT AUTO_INCREMENT PRIMARY KEY,
            titulo VARCHAR(255) NOT NULL,
            categoria VARCHAR(50) NOT NULL,
            nota DECIMAL(2,1) NOT NULL
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()

def validar_nota():
    while True:
        try:
            nota = float(input("Digite a nota (0.5 a 5.0): "))
            if 0.5 <= nota <= 5.0 and nota % 0.5 == 0:
                return nota
            print("Erro: A nota deve ser entre 0.5 e 5.0, em passos de 0.5.")
        except ValueError:
            print("Erro: Digite um número válido (ex: 4.5).")

def adicionar_registro():
    conn = conectar()
    if not conn: return
    
    print("\n--- Nova Avaliação ---")
    titulo = input("Nome da obra: ")
    categoria = input("Categoria (Jogo, Filme ou Série): ")
    nota = validar_nota()

    cursor = conn.cursor()
    query = "INSERT INTO avaliacoes (titulo, categoria, nota) VALUES (%s, %s, %s)"
    cursor.execute(query, (titulo, categoria, nota))
    conn.commit()
    
    print("Salvo no banco de dados!")
    cursor.close()
    conn.close()

def listar_registros():
    conn = conectar()
    if not conn: return

    cursor = conn.cursor()
    cursor.execute("SELECT categoria, titulo, nota FROM avaliacoes")
    registros = cursor.fetchall()

    print("\n--- Suas Avaliações ---")
    if not registros:
        print("Nada encontrado no banco.")
    else:
        for (cat, tit, nota) in registros:
            print(f"[{cat}] {tit} - Nota: {float(nota)}")

    cursor.close()
    conn.close()

def menu():
    inicializar_banco()
    while True:
        print("\n=== SISTEMA DE AVALIAÇÕES ===")
        print("1. Avaliar nova obra")
        print("2. Ver minhas avaliações")
        print("3. Sair")
        
        escolha = input("Escolha: ")
        if escolha == '1': adicionar_registro()
        elif escolha == '2': listar_registros()
        elif escolha == '3': break
        else: print("Opção inválida.")

if __name__ == "__main__":
    menu()