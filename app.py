from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

config = {
    'host': 'localhost',
    'user': 'kadu',       
    'password': '1234',       
    'database': 'sistema_avaliacoes'
}

def conectar():
    return mysql.connector.connect(**config)

def inicializar_banco():
    conn = conectar()
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
    
    try:
        cursor.execute("ALTER TABLE avaliacoes ADD COLUMN coracao BOOLEAN DEFAULT FALSE")
    except:
        pass
        
    conn.commit()
    cursor.close()
    conn.close()

@app.route('/')
def index():
    inicializar_banco()
    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM avaliacoes ORDER BY id DESC")
    avaliacoes = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return render_template('index.html', avaliacoes=avaliacoes)

@app.route('/adicionar', methods=['POST'])
def adicionar():
    titulo = request.form['titulo']
    categoria = request.form['categoria']
    nota = request.form['nota']
    coracao = 1 if request.form.get('coracao') else 0

    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO avaliacoes (titulo, categoria, nota, coracao) VALUES (%s, %s, %s, %s)", (titulo, categoria, nota, coracao))
    conn.commit()
    cursor.close()
    conn.close()

    return redirect('/')

@app.route('/deletar/<int:id>', methods=['POST'])
def deletar(id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM avaliacoes WHERE id = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)