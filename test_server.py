import pytest
import _mysql_connector
from unittest.mock import patch, MagicMock

@pytest.fixture
def app():
    from server import app
    app.config.update({
        "TESTING": True,
    })
    
    yield app

# criando client
@pytest.fixture
def client(app):
    app.config['TESTING'] = True
    return app.test_client()


def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.get_json() == {"mensagem": "Conexao bem sucedida"}

#criando teste para rota filtrando por cidade
@patch('server.conectando_db')
def test_por_cidade_passa(mock_conectando_db, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.fetchall.return_value = [
        {"id": 1, "logradouro": "José", "tipo_logradouro": "Rua", "bairro": "Cohab", "cidade": "Bofete", "cep": 18590-000, "tipo": "casa", "valor": 150000, "data_aquisicao": "2025-05-10"},
    ]

    mock_conectando_db.return_value = mock_conn

    response = client.get("/cidade")

    assert response.status_code == 200

    expected_response = {
        "filtrado": [
            {"id": 1, "logradouro": "José", "tipo_logradouro": "Rua", "bairro": "Cohab", "cidade": "Bofete", "cep": "18590-000", "tipo": "casa", "valor": 150000, "data_aquisicao": "2025-05-10"},
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

def test_busca_por_cidade_sem_parametro(client):
    response = client.post('/cidade', data={})
    assert response.status_code == 400
    assert response.json == {'erro': 'Nenhuma cidade foi fornecida'}

@patch('server.conectando_db')
def test_por_cidade_nao_passa(mock_conectando_db, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.fetchall.return_value = []

    mock_conectando_db.return_value = mock_conn

    response = client.get('/cidade')

    assert response.status_code == 404
    assert response.get_json() == {"mensagem": "Nao foi possivel filtrar o imovel"}

# criando o teste para filtrar por tipo
@patch('server.conectando_db')
def test_por_tipo_passa(mock_conectando_db, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.fetchall.return_value = [
        {"id": 1, "bairro": "Um bairro ai", "cidade": "Uma Cidade", "tipo": "apartamento"},
        {"id": 2, "bairro": "Um bairro ai", "cidade": "Uma Cidade", "tipo": "apartamento"},
    ]


    mock_conectando_db.return_value = mock_conn

    response = client.get("/tipo")

    assert response.status_code == 200

    expected_response = {
        "filtrado": [
            {"id": 1, "bairro": "Um bairro ai", "cidade": "Uma Cidade", "tipo": "apartamento"},
            {"id": 2, "bairro": "Um bairro ai", "cidade": "Uma Cidade", "tipo": "apartamento"},
        ]
    }
    assert response.get_json() == expected_response["filtrado"]

@patch("server.conectando_db")
def test_por_tipo_nao_passa(mock_conectando_db, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.fetchall.return_value = []

    mock_conectando_db.return_value = mock_conn

    response = client.get("/tipo")

    assert response.status_code == 404
    assert response.get_json() == {"mensagem": "Nao foi possivel filtrar o imovel"}

# fazendo o teste de remover um item do banco de dados
@patch('server.conectando_db')
def test_remover_db_passa(mock_get, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.rowcount = 1

    mock_get.return_value = mock_conn
    mock_get.return_value.status_code = 200

    response = client.get('/remover')

    assert response.status_code == 200

    assert response.get_json() == {"mensagem": "Imovel removido com sucesso"}

@patch('server.conectando_db')
def test_remover_db_nao_passa(mock_get, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.rowcount = 0

    mock_get.return_value = mock_conn
    mock_get.return_value.status_code = 404

    response = client.get('/remover')

    assert response.status_code == 404

    assert response.get_json() == {"mensagem": "Nao foi possivel remover o imovel"}

   
    
