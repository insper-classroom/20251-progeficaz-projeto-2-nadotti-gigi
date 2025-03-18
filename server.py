from flask import Flask, jsonify, request
# from flask_restful import Api
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv(override=True)

app = Flask(__name__)

db_config = {
    'host': f"{os.getenv('HOST')}",  
    'port': int(os.getenv('PORT')),  
    'user': f"{os.getenv('USER')}",  
    'password': f"{os.getenv('PASSWORD')}",  
    'database': f"{os.getenv('DB')}",
    # 'ssl_ca': 'ca.pem'
    }

def conectando_db():
    try:
        print("Tentando conectar ao banco...")
        connection = mysql.connector.connect(**db_config)
        print("Conexão bem-sucedida!")
    except mysql.connector.Error as err:
        print(f"Erro de MySQL: {err}")
        sys.exit(1)
    except Exception as e:
        print(f"Erro inesperado: {e}")
        sys.exit(1)

    print("Se esse print aparecer, a conexão funcionou.")

    print("conectou")
    return connection
    
@app.route('/')
def index():
    print("oi")
    conexao = conectando_db()
    print("oi depois")
    if conexao:
        return jsonify({'mensagem': 'Conexao bem sucedida'})
    
    else:
        return jsonify({'erro': f'{conexao}'}), 500
    
@app.route('/cidade', methods=['POST', 'GET'])
def por_cidade():
    conn = conectando_db()
    cursor = conn.cursor(dictionary=True)

    cidade_selecionada = request.form.get('cidade')
    cursor.execute("SELECT * FROM imoveis WHERE cidade = %s", (cidade_selecionada,))
    response = cursor.fetchall()

    return jsonify(response), 200

if __name__ =='__main__':
    app.run(debug=True)