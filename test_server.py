import pytest
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
        {"id": 1, "bairro": "Um bairro ai", "cidade": "Uma Cidade"},
        {"id": 2, "bairro": "Um bairro ai", "cidade": "Uma Cidade"},
    ]


    mock_conectando_db.return_value = mock_conn

    response = client.get("/cidade")

    assert response.status_code == 200

    expected_response = {
        "filtrado": [
            {"id": 1, "bairro": "Um bairro ai", "cidade": "Uma Cidade"},
            {"id": 2, "bairro": "Um bairro ai", "cidade": "Uma Cidade"},
        ]
    }
    assert response.get_json() == expected_response["filtrado"]

def test_por_cidade_nao_passa(client):

    with patch("server.conectando_db") as mock_get:
        mock_get.return_value.status_code = 404
    response = client.get("/cidade")


    assert response.status_code == 404
    assert response.get_json() == {"mensagem" : "Nao foi possivel filtrar o imovel"}


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

def test_por_tipo_nao_passa(client):

    with patch("server.conectando_db") as mock_get:
        mock_get.return_value.status_code = 404
    response = client.get("/cidade")


    assert response.status_code == 404
    assert response.get_json() == {"mensagem" : "Nao foi possivel filtrar o imovel"}


