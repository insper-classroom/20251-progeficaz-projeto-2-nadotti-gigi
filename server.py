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
    
@app.route('/cidade', methods=['GET'])
def por_cidade():
    conn = conectando_db()


    cursor = conn.cursor(dictionary=True)

    cidade_selecionada = 'Limeira'

    if cidade_selecionada:
        cursor.execute("SELECT * FROM imoveis WHERE cidade = %s", (cidade_selecionada,))  
        response = cursor.fetchall()
        print(len(response))       
        if len(response) > 0:  
            return jsonify(response), 200  
        else:
            return jsonify({"mensagem": "Nao foi possivel filtrar o imovel"}), 404  

    return jsonify({"mensagem": "Nao foi possivel filtrar o imovel"}), 400  

@app.route('/tipo', methods=['GET'])
def por_tipo():
    conn = conectando_db()


    cursor = conn.cursor(dictionary=True)

    tipo_selecionado = 'apartamento'

    if tipo_selecionado:
        cursor.execute("SELECT * FROM imoveis WHERE tipo = %s", (tipo_selecionado))  
        response = cursor.fetchall()
        print(len(response))       
        if len(response) > 0:  
            return jsonify(response), 200  
        else:
            return jsonify({"mensagem": "Nao foi possivel filtrar o imovel"}), 404  

    return jsonify({"mensagem": "Nao foi possivel filtrar o imovel"}), 400  



if __name__ =='__main__':
    app.run(debug=True)
