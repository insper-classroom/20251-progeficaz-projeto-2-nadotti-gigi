from flask import Flask, jsonify, request
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
        cursor.execute("SELECT * FROM imoveis WHERE tipo = %s", (tipo_selecionado,))
        response = cursor.fetchall()
        print(len(response))       
        if len(response) > 0:  
            return jsonify(response), 200  
        else:
            return jsonify({"mensagem": "Nao foi possivel filtrar o imovel"}), 404  

    return jsonify({"mensagem": "Nao foi possivel filtrar o imovel"}), 404  

@app.route('/remover', methods=['GET'])
def remover():
    conn = conectando_db()

    cursor = conn.cursor(dictionary=True)
    id_imovel = 2

    if id_imovel:
        cursor.execute(f"DELETE FROM imoveis WHERE id = {id_imovel}")
        conn.commit()
        
        if cursor.rowcount > 0:
            print(cursor.rowcount)
            return {"mensagem": "Imovel removido com sucesso"}, 200
        
        else:
            return {"mensagem": "Nao foi possivel remover o imovel"}, 404

if __name__ =='__main__':
    app.run(debug=True)