from flask import Flask, jsonify
import mysql.connector

app = Flask(__name__)

db_config = {
    'host': 'mysql-projeto2insperborabill-nadottipedro5-2430.d.aivencloud.com',  
    'port': 11430,  
    'user': 'avnadmin',  
    'password': 'AVNS_1ytLtPwTE9TM-m8NhnW',  
    'database': 'MyImoveis'
    }

def conectando_db():
    try:
        connection = mysql.connector.connect(**db_config)
        return connection
    except mysql.connector.Error as err:
        print(f"Falha na conexao: {err}")
        return None
    

@   app.route('/')
def index():
    conexao = conectando_db()
    if conexao:
        return jsonify({'mensagem': 'Conexao bem sucedida'})
    
    else:
        return jsonify({'erro': 'Deu B.O na conexao ein'}), 500
    
if __name__ =='__main__':
    app.run(debug=True)