from flask import Flask, jsonify, request
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv(override=True)

app = Flask(__name__)

db_config = {
    'host': os.getenv('HOST'),
    'port': int(os.getenv('PORT')),  
    'user': os.getenv('USER'),  
    'password': os.getenv('PASSWORD'),  
    'database': os.getenv('DB'),
    }

def conectando_db():
    try:
        print("Tentando conectar ao banco...")
        connection = mysql.connector.connect(**db_config)
        print("Conexão bem-sucedida!")
        return connection
    except mysql.connector.Error as err:
        print(f"Erro de MySQL: {err}")
        return None
        # sys.exit(1)
    except Exception as e:
        print(f"Erro inesperado: {e}")
        return None
        # sys.exit(1)

    # print("Se esse print aparecer, a conexão funcionou.")

    # print("conectou")
    # return connection
    
@app.route('/imoveis')
def get_imoveis():
    conexao = conectando_db()
    if conexao:
        cursor = conexao.cursor(dictionary=True)
        cursor.execute("SELECT * FROM imoveis")
        response = cursor.fetchall()
        return jsonify(response), 200
    else:
        return jsonify({'erro': 'Falha na conexão'}), 500
    

@app.route('/imoveis/<int:id_imovel>', methods=['GET'])
def obter_imovel_por_id(id_imovel):
    conn = conectando_db()
    if not conn:
        return jsonify({'erro': 'Falha na conexão com o banco de dados'}), 500
    
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM imoveis WHERE id = %s", (id_imovel,))
    imovel = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    if imovel:
        return jsonify(imovel), 200
    else:
        return jsonify([]), 404


@app.route('/imoveis/cidade/<string:cidade>', methods=['GET'])
def por_cidade(cidade: str):
    conn = conectando_db()
    if not conn: return jsonify({'erro': 'Falha na conexão com o banco de dados'}), 500

    cursor = conn.cursor(dictionary=True)


    if cidade:
        cursor.execute(f"SELECT * FROM imoveis WHERE cidade = '{cidade}'")  
        response = cursor.fetchall() 
        if len(response) > 0:  
            return jsonify(response), 200  
        else:
            return jsonify([]), 404  

    return jsonify({"mensagem": "Nao foi possivel fazer o bagulho"}), 400  


@app.route('/imoveis/tipo/<string:tipo>', methods=['GET'])
def por_tipo(tipo: str):
    conn = conectando_db()


    cursor = conn.cursor(dictionary=True)


    if tipo:
        cursor.execute(f"SELECT * FROM imoveis WHERE tipo = {tipo}")
        response = cursor.fetchall()
        print(len(response))       
        if len(response) > 0:  
            return jsonify(response), 200  
        else:
            return jsonify([]), 404  

    return jsonify({"mensagem": "Nao foi possivel filtrar o imovel"}), 404  


@app.route('/imoveis', methods=['DELETE'])
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

@app.route('/imoveis', methods=['POST'])
def adicionar_imovel():
    conn = conectando_db()
    if not conn:
        return jsonify({'erro': 'Falha na conexão com o banco de dados'}), 500
    
    dados = request.get_json()
    
    # Validação básica dos dados
    campos_necessarios = ['logradouro', 'tipo_logradouro', 'bairro', 'cidade', 'cep', 'tipo', 'valor']
    for campo in campos_necessarios:
        if campo not in dados:
            return jsonify({'erro': f'Campo obrigatório ausente: {campo}'}), 400
    
    cursor = conn.cursor()
    
    try:
        query = """
        INSERT INTO imoveis (logradouro, tipo_logradouro, bairro, cidade, cep, tipo, valor, data_aquisicao)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        valores = (
            dados['logradouro'],
            dados['tipo_logradouro'],
            dados['bairro'],
            dados['cidade'],
            dados['cep'],
            dados['tipo'],
            dados['valor'],
            dados.get('data_aquisicao')  # Campo opcional
        )
        
        cursor.execute(query, valores)
        conn.commit()
        
        novo_id = cursor.lastrowid
        
        cursor.close()
        conn.close()
        
        return jsonify({"id": novo_id, "mensagem": "Imóvel adicionado com sucesso"}), 201
    
    except Exception as e:
        conn.rollback()
        return jsonify({"erro": f"Erro ao adicionar imóvel: {str(e)}"}), 500
if __name__ =='__main__':
    app.run(debug=True)