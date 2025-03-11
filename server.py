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
        return jsonify({'mensagem': f'{conexao}'})
    
    else:
        return jsonify({'erro': f'{conexao}'}), 500
    
@app.route('/cidade', methods=['POST', 'GET'])
def por_cidade():
    connection = conectando_db()
    cursor = connection.cursor(dictionary=True)
    

    cidade_selecionada = request.form.get('cidade')
    
    if cidade_selecionada:
        cursor.execute(f"SELECT * FROM MyImoveis WHERE cidade = {cidade_selecionada}")
    else:
        cursor.execute("SELECT * FROM MyImoveis")

    return jsonify({"mensagem": "bagulho"})

if __name__ =='__main__':
    app.run(debug=True)
