from flask import Flask, jsonify, request
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

db_config = {
    'host': f"{os.getenv('HOST')}",  
    'port': os.getenv('PORT'),  
    'user': f"{os.getenv('USER')}",  
    'password': f"{os.getenv('PASSWORD')}",  
    'database': f"{os.getenv('DB')}"
    }

def conectando_db():
    connection = mysql.connector.connect(**db_config)
    return connection
    
    

@app.route('/')
def index():
    conexao = conectando_db()
    if conexao:
        return jsonify({'mensagem': 'Conexao bem sucedida'})
    
    else:
        return jsonify({'erro': f'{conexao}'}), 500
    
@app.route('/cidade', methods=['POST', 'GET'])
def por_cidade():
    conn = conectando_db()
    cursor = conn.cursor(dictionary=True)

    cidade_selecionada = request.form.get('cidade')

    cursor.execute(f"SELECT * FROM imoveis WHERE cidade = {cidade_selecionada}")
    response = cursor.fetchall()

    return jsonify(response), 200


if __name__ =='__main__':
    app.run(debug=True)
