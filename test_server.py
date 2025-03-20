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

# teste para conexao
@patch('server.conectando_db')
def test_get_imoveis(mock_conectando_db, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.fetchall.return_value = [
            {"id": 1, "logradouro": "Mariana Gomes", "tipo_logradouro": "Rua", "bairro": "Itaim Bibi", "cidade": "São Paulo", "cep": "04550004", "tipo": "apartamento", "valor": "123425", "data_aquisicao":"2017-07-29"},
            {"id": 2, "logradouro": "Lorenzo Flosi", "tipo_logradouro": "Avenida", "bairro": "Vila Olimpia", "cidade": "São Paulo", "cep": "04545004", "tipo": "apartamento", "valor": "458609", "data_aquisicao": "2024-04-10"},
        ]


    mock_conectando_db.return_value = mock_conn

    response = client.get('/imoveis')

    expected_response = {
        "imovel": [
            {"id": 1, "logradouro": "Mariana Gomes", "tipo_logradouro": "Rua", "bairro": "Itaim Bibi", "cidade": "São Paulo", "cep": "04550004", "tipo": "apartamento", "valor": "123425", "data_aquisicao":"2017-07-29"},
            {"id": 2, "logradouro": "Lorenzo Flosi", "tipo_logradouro": "Avenida", "bairro": "Vila Olimpia", "cidade": "São Paulo", "cep": "04545004", "tipo": "apartamento", "valor": "458609", "data_aquisicao": "2024-04-10"},
        ]
    }

    assert response.status_code == 200
    assert response.get_json() == expected_response['imovel']



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

    response = client.get("/imoveis/cidade/Bofete")

    assert response.status_code == 200

    expected_response = {
        "filtrado": [
            {"id": 1, "logradouro": "José", "tipo_logradouro": "Rua", "bairro": "Cohab", "cidade": "Bofete", "cep": 18590-000, "tipo": "casa", "valor": 150000, "data_aquisicao": "2025-05-10"},
        ]
    }
    assert response.get_json() == expected_response["filtrado"]


# teste pos cidade nao passa
@patch('server.conectando_db')
def test_por_cidade_nao_passa(mock_conectando_db, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.fetchall.return_value = []

    mock_conectando_db.return_value = mock_conn
    

    response = client.get('imoveis/cidade/Judymouth')

    assert response.status_code == 404
    assert response.get_json() == []


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

    response = client.get("/imoveis/tipo/apartamento")

    assert response.status_code == 200

    expected_response = {
        "filtrado": [
            {"id": 1, "bairro": "Um bairro ai", "cidade": "Uma Cidade", "tipo": "apartamento"},
            {"id": 2, "bairro": "Um bairro ai", "cidade": "Uma Cidade", "tipo": "apartamento"},
        ]
    }
    assert response.get_json() == expected_response["filtrado"]


# teste por tipo nao passa
@patch("server.conectando_db")
def test_por_tipo_nao_passa(mock_conectando_db, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.fetchall.return_value = []

    mock_conectando_db.return_value = mock_conn

    response = client.get("imoveis/tipo/fazenda")

    assert response.status_code == 404
    assert response.get_json() == []


# fazendo o teste de remover um item do banco de dados
@patch('server.conectando_db')
def test_remover_db_passa(mock_get, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.rowcount = 1

    mock_get.return_value = mock_conn
    mock_get.return_value.status_code = 200

    response = client.delete('/imoveis')

    assert response.status_code == 200

    assert response.get_json() == {"mensagem": "Imovel removido com sucesso"}

# teste remover nao passa
@patch('server.conectando_db')
def test_remover_db_nao_passa(mock_get, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.rowcount = 0

    mock_get.return_value = mock_conn
    mock_get.return_value.status_code = 404

    response = client.delete('/imoveis')

    assert response.status_code == 404

    assert response.get_json() == {"mensagem": "Nao foi possivel remover o imovel"}

# teste por id passa
@patch('server.conectando_db')
def test_obter_imovel_por_id(mock_conectando_db, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.fetchone.return_value = [
            {"id": 1, "logradouro": "nadottins", "tipo_logradouro": "Rua", "bairro": "Itaim Bibi", "cidade": "São Paulo", "cep": "04550004", "tipo": "apartamento", "valor": "123425", "data_aquisicao":"2017-07-29"}
        ]


    mock_conectando_db.return_value = mock_conn

    response = client.get('/imoveis/1')

    expected_response = {
        "imovel": [
            {"id": 1, "logradouro": "nadottins", "tipo_logradouro": "Rua", "bairro": "Itaim Bibi", "cidade": "São Paulo", "cep": "04550004", "tipo": "apartamento", "valor": "123425", "data_aquisicao":"2017-07-29"}
        ]
    }

    assert response.status_code == 200
    assert response.get_json() == expected_response['imovel']

# teste por id nao passa
@patch('server.conectando_db')
def test_obter_imovel_por_id_falhou(mock_conectando_db, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.fetchone.return_value = [
    
     ]

    mock_conectando_db.return_value = mock_conn

    response = client.get('/imoveis/2')

    expected_response = {
        "imovel": [

        ]}

    assert response.status_code == 404
    assert response.get_json() == expected_response['imovel']

@patch("server.conectando_db")
def test_adicionar_imovel(mock_connect_db, client):

    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_conn.cursor.return_value = mock_cursor

    mock_connect_db.return_value = mock_conn
 
    response = client.post('/imoveis', json={"logradouro": "Miguel Damha", "tipo_logradouro": "Avenida", "bairro": "Damha", "cidade": "São José do Rio Preto", "cep": "15061-800", "tipo": "casa em condominio", "valor": 50000, "data_aquisicao": "2025-03-11"})

    assert response.status_code == 200
    assert response.get_json() == {"mensagem": "imovel adicionado com sucesso"}

@patch("servidor.conectando_db")
def test_atualiza_imovel(mock_connect_db, imovel):

    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.fetchall.side_effect = [
        [(1, "Vereador", "Rua", "Centro", "Bofete", "18590-000", "casa", 50000, "2025-03-11")],  # Imóvel existe
        ['id','logradouro', 'tipo_logradouro', 'bairro','cidade', 'cep','tipo', 'valor', 'data_aquisicao']
    ]

    mock_connect_db.return_value = mock_conn

    response = imovel.put("/imoveis/atualiza/1/tipo/apartamento")

    assert response.status_code == 200

    expected_response = {
        'mensagem': 'Imóvel atualizado com sucesso.'
    }

    assert response.get_json() == expected_response