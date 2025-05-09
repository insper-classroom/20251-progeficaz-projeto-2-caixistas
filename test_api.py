import pytest
from unittest.mock import patch, MagicMock
from servidor import app, connect_db

@pytest.fixture
def imovel():
    app.config["TESTING"] = True
    with app.test_client() as imovel:
        yield imovel

@patch("servidor.connect_db")
def test_get_imoveis(mock_connect_db, imovel):

    # Criação do Mock para a conexão e cursor
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    # O mock retorna o cursor quando chamamos o conn.cursor()
    mock_conn.cursor.return_value = mock_cursor

    # Simulação do banco de dados
    mock_cursor.fetchall.return_value = [
        (1, "Vereador", "Rua", "Centro", "Bofete", "18590-000", "casa", 50000, "2025-03-11"),
        (2, "Miguel Damha", "Avenida", "Damha", "São José do Rio Preto", "15061-800", "casa em condominio", 50000, "2025-03-11"),
    ]

    #Chama a conexão do Mock ao invés da conexão real
    mock_connect_db.return_value = mock_conn

    # Faz a requisição GET para a API na rota /imoveis
    response = imovel.get("/imoveis")

    # Vendo se o status da resposta é 200
    assert response.status_code == 200

    # Respostas esperadas
    expected_response = {
        "imovel": [
            {"id": 1, "logradouro": "Vereador", "tipo_logradouro": "Rua", "bairro": "Centro", "cidade": "Bofete", "cep": "18590-000", "tipo": "casa", "valor": 50000, "data_aquisicao": "2025-03-11"},
            {"id": 2, "logradouro": "Miguel Damha", "tipo_logradouro": "Avenida", "bairro": "Damha", "cidade": "São José do Rio Preto", "cep": "15061-800", "tipo": "casa em condominio", "valor": 50000, "data_aquisicao": "2025-03-11"},
        ]
    }

    assert response.get_json() == expected_response

@patch("servidor.connect_db")
def test_delete_imovel(mock_connect_db, imovel):

    # Criação do Mock para a conexão e cursor
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    # O mock retorna o cursor quando chamamos o conn.cursor()
    mock_conn.cursor.return_value = mock_cursor

    # Mock para a exclusão (não retorna nada)
    mock_cursor.execute.return_value = None

    # Simulação do banco de dados após a exclusão
    mock_cursor.fetchall.side_effect = [
        [
            (1, "Vereador", "Rua", "Centro", "Bofete", "18590-000", "casa", 50000, "2025-03-11"),
            (2, "Miguel Damha", "Avenida", "Damha", "São José do Rio Preto", "15061-800", "casa em condominio", 50000, "2025-03-11"),
        ]
    ]

    # Mock da conexão
    mock_connect_db.return_value = mock_conn

    # Faz a requisição DELETE
    response = imovel.delete("/imoveis/delete/1")
    
    assert response.status_code == 200
    
    expected_response = {
        'mensagem': 'Imóvel removido com sucesso.'
    }

    assert response.get_json() == expected_response

@pytest.fixture
def imovel_id():
    app.config["TESTING"] = True
    with app.test_client() as imovel:
        yield imovel
    
@patch("servidor.connect_db")
def test_get_imoveis_id(mock_connect_db, imovel):

    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    # O mock retorna o cursor quando chamamos o conn.cursor()
    mock_conn.cursor.return_value = mock_cursor

    # Mock para a exclusão (não retorna nada)
    mock_cursor.execute.return_value = None

    # Simulação do banco de dados
    mock_cursor.fetchall.return_value = [
        (1, "Vereador", "Rua", "Centro", "Bofete", "18590-000", "casa", 50000, "2025-03-11"),
        (2, "Miguel Damha", "Avenida", "Damha", "São José do Rio Preto", "15061-800", "casa em condominio", 50000, "2025-03-11"),
    ]

    #Chama a conexão do Mock ao invés da conexão real
    mock_connect_db.return_value = mock_conn

    # Faz a requisição GET para a API na rota /id
    response = imovel.get("/imoveis/1")

    # Vendo se o status da resposta é 200
    assert response.status_code == 200

    # Respostas esperadas
    expected_response = {
        "imovel": [
            {"id": 1, "logradouro": "Vereador", "tipo_logradouro": "Rua", "bairro": "Centro", "cidade": "Bofete", "cep": "18590-000", "tipo": "casa", "valor": 50000, "data_aquisicao": "2025-03-11"},
        ]
    }

    assert response.get_json() == expected_response

@pytest.fixture
def imovel_tipo():
    app.config["TESTING"] = True
    with app.test_client() as imovel:
        yield imovel
    
@patch("servidor.connect_db")
def test_get_imoveis_tipo(mock_connect_db, imovel):

    # Criação do Mock para a conexão e cursor
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    # O mock retorna o cursor quando chamamos o conn.cursor()
    mock_conn.cursor.return_value = mock_cursor

    # Simulação do banco de dados
    mock_cursor.fetchall.return_value = [
        (1, "Vereador", "Rua", "Centro", "Bofete", "18590-000", "casa", 50000, "2025-03-11"),
        (2, "Miguel Damha", "Avenida", "Damha", "São José do Rio Preto", "15061-800", "casa em condominio", 50000, "2025-03-11"),
    ]

    #Chama a conexão do Mock ao invés da conexão real
    mock_connect_db.return_value = mock_conn

    # Faz a requisição GET para a API na rota /
    response = imovel.get("/imoveis/tipo/casa")

    # Vendo se o status da resposta é 200
    assert response.status_code == 200

    # Respostas esperadas
    expected_response = {
        "imovel": [
            {"id": 1, "logradouro": "Vereador", "tipo_logradouro": "Rua", "bairro": "Centro", "cidade": "Bofete", "cep": "18590-000", "tipo": "casa", "valor": 50000, "data_aquisicao": "2025-03-11"},
        ]
    } 

    assert response.get_json() == expected_response

@patch("servidor.connect_db")
def test_atualiza_imovel(mock_connect_db, imovel):

    # Criação do Mock para a conexão e cursor
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    # O mock retorna o cursor quando chamamos o conn.cursor()
    mock_conn.cursor.return_value = mock_cursor

    # Simulação do banco de dados para verificar se o imóvel existe
    mock_cursor.fetchall.side_effect = [
        [(1, "Vereador", "Rua", "Centro", "Bofete", "18590-000", "casa", 50000, "2025-03-11")],  # Imóvel existe
        ['id','logradouro', 'tipo_logradouro', 'bairro','cidade', 'cep','tipo', 'valor', 'data_aquisicao']
    ]

    # Mock da conexão
    mock_connect_db.return_value = mock_conn

    # Faz a requisição PUT para a API na rota /imoveis/atualiza/1/tipo/apartamento
    response = imovel.put("/imoveis/atualiza/1/tipo/apartamento")

    # Vendo se o status da resposta é 200
    assert response.status_code == 200

    # Respostas esperadas
    expected_response = {
        'mensagem': 'Imóvel atualizado com sucesso.'
    }

    assert response.get_json() == expected_response
    
@pytest.fixture
def imovel_cidade():
    app.config["TESTING"] = True
    with app.test_client() as imovel:
        yield imovel
    
@patch("servidor.connect_db")
def test_get_imoveis_cidade(mock_connect_db, imovel):

    # Criação do Mock para a conexão e cursor
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    # O mock retorna o cursor quando chamamos o conn.cursor()
    mock_conn.cursor.return_value = mock_cursor

    # Simulação do banco de dados
    mock_cursor.fetchall.return_value = [
        (2, "Miguel Damha", "Avenida", "Damha", "São José do Rio Preto", "15061-800", "casa em condominio", 50000, "2025-03-11")
    ]

    #Chama a conexão do Mock ao invés da conexão real
    mock_connect_db.return_value = mock_conn

    # Faz a requisição GET para a API na rota /cidade
    response = imovel.get("/imoveis/cidade/São José do Rio Preto")

    # Vendo se o status da resposta é 200
    assert response.status_code == 200

    # Respostas esperadas
    expected_response = {
        "imovel": [
            {"id": 2, "logradouro": "Miguel Damha", "tipo_logradouro": "Avenida", "bairro": "Damha", "cidade": "São José do Rio Preto", "cep": "15061-800", "tipo": "casa em condominio", "valor": 50000, "data_aquisicao": "2025-03-11"},
        ]
    } 

    assert response.get_json() == expected_response

@pytest.fixture
def adiciona_imovel():
    app.config["TESTING"] = True
    with app.test_client() as imovel:
        yield imovel
    
@patch("servidor.connect_db")
def test_post_imoveis(mock_connect_db, imovel):

    # Criação do Mock para a conexão e cursor
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    # O mock retorna o cursor quando chamamos o conn.cursor()
    mock_conn.cursor.return_value = mock_cursor
    #Chama a conexão do Mock ao invés da conexão real
    mock_connect_db.return_value = mock_conn
 
    # Simulação do banco de dados
    response = imovel.post('/imoveis', json={"logradouro": "Miguel Damha", "tipo_logradouro": "Avenida", "bairro": "Damha", "cidade": "São José do Rio Preto", "cep": "15061-800", "tipo": "casa em condominio", "valor": 50000, "data_aquisicao": "2025-03-11"})

    # Vendo se o status da resposta é 200
    assert response.status_code == 200
    assert response.get_json() == {"mensagem": "imovel adicionado com sucesso"}
