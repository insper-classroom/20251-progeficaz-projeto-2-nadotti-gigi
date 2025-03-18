import pytest
import _mysql_connector
from unittest.mock import patch, MagicMock
from server import app, conectando_db

@pytest.fixture()
def app():
    from server import app
    app.config.update({
        "TESTING": True,
    })
    
    yield app

# criando client
@pytest.fixture()
def client(app):
    app.config['TESTING'] = True
    return app.test_client()


def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.get_json() == {"mensagem": "Conexao bem sucedida"}

#criando teste para rota filtrando por cidade
@patch('server.conectando_db')
def test_por_cidade(mock_conectando_db, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    # Configuramos o Mock para retornar o cursor quando chamarmos conn.cursor()
    mock_conn.cursor.return_value = mock_cursor

    # Simulamos o retorno do banco de dados
    mock_cursor.fetchall.return_value = [
        (1, "José", "Rua", "Cohab" "Bofete", "18590-000", "casa", 150000, "2025-05-10"),
        (2, "Casil", "Avenida", "Vila Olímpia" "São Paulo", "04506-003", "apartamento", 150000, "2025-05-10"),
        # {"id": 2, "bairro": "Um bairro ai", "cidade": "Uma Cidade"},
    ]

    # Substituímos a função `connect_db` para retornar nosso Mock em vez de uma conexão real
    mock_conectando_db.return_value = mock_conn

    # Fazemos a requisição para a API
    response = client.get("/Bofete")

    # Verificamos se o código de status da resposta é 200 (OK)
    assert response.status_code == 200

    # Verificamos se os dados retornados estão corretos
    expected_response = {
        "filtrado": [
            {"id": 1, "logradouro": "José", "tipo_logradouro": "Rua", "bairro": "Cohab", "cidade": "Bofete", "cep": "18590-000", "tipo": "casa", "valor": 150000, "data_aquisicao": "2025-05-10"},
            # {"id": 2, "bairro": "Um bairro ai", "cidade": "Uma Cidade"},
        ]
    }
    assert response.get_json() == expected_response

# testa se a conexão funcionou ou não
def test_conexao_sucedida(client):
    with patch('server.conectando_db') as mock_db:

        mock_db.return_value = True
        response = client.get('/')
        assert response.status_code == 200
        assert response.json == {'mensagem': 'Conexao bem sucedida'}

def test_conexao_falha(client):
    with patch('server.conectando_db') as mock_db:
        mock_db.return_value = None 
        response = client.get('/')
        assert response.status_code == 500
        assert response.json == {'erro': 'Falha na conexão com o banco de dados'}

def test_busca_por_cidade_sucesso(client):
    mock_data = [{'id': 1, 'cidade': 'São Paulo', 'preco': 200000}]

    with patch('server.conectando_db') as mock_db:
        mock_conn = mock_db.return_value
        mock_cursor = mock_conn.cursor.return_value
        mock_cursor.fetchall.return_value = mock_data 

        response = client.get('/cidade', data={'cidade': 'São Paulo'})
        assert response.status_code == 200
        assert response.json == mock_data

def test_busca_por_cidade_sem_parametro(client):
    response = client.post('/cidade', data={})
    assert response.status_code == 400
    assert response.json == {'erro': 'Nenhuma cidade foi fornecida'}

def test_busca_por_cidade_falha_conexao(client):
    with patch('server.conectando_db') as mock_db:
        mock_db.return_value = None
        response = client.get('/cidade', data={'cidade': 'São Paulo'})

        assert response.status_code == 500
        assert response.json == {'erro': 'Não foi possível conectar ao banco de dados'}