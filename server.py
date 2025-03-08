from flask import Flask, jsonify
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
    try:
        connection = mysql.connector.connect(**db_config)
        return connection
    except mysql.connector.Error as err:
        print(f"Falha na conexao: {err}")
        return None
    

@app.route('/')
def index():
    conexao = conectando_db()
    if conexao:
        return jsonify({'mensagem': 'Conexao bem sucedida'})
    
    else:
        return jsonify({'erro': 'Deu B.O na conexao ein'}), 500
    
if __name__ =='__main__':
    app.run(debug=True)
