import pytest
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
        {"id": 1, "bairro": "Um bairro ai", "cidade": "Uma Cidade"},
        {"id": 2, "bairro": "Um bairro ai", "cidade": "Uma Cidade"},
    ]


    # Substituímos a função `connect_db` para retornar nosso Mock em vez de uma conexão real
    mock_conectando_db.return_value = mock_conn

    # Fazemos a requisição para a API
    response = client.get("/cidade")

    # Verificamos se o código de status da resposta é 200 (OK)
    assert response.status_code == 200

    # Verificamos se os dados retornados estão corretos
    expected_response = {
        "filtrado": [
            {"id": 1, "bairro": "Um bairro ai", "cidade": "Uma Cidade"},
            {"id": 2, "bairro": "Um bairro ai", "cidade": "Uma Cidade"},
        ]
    }
    assert response.get_json() == expected_response["filtrado"]
