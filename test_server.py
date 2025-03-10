import pytest

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

def test_por_cidade(client):
    response = client.get('/por-cidade/Limeira')
    assert response.status_code == 200
    filtrado = response.get_json()
    assert filtrado["cidades"] == "Limeira"
