"""
Fixtures compartilhadas por todos os arquivos de teste.

Os testes usam um banco SEPARADO (bulbe_test.db), nunca o banco de
desenvolvimento. Por isso a variavel de ambiente e definida aqui,
ANTES de qualquer import de "app".
"""

import os

os.environ["BULBE_DATABASE_URL"] = "sqlite:///./bulbe_test.db"

import pytest  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

from app.db.database import Base, engine  # noqa: E402
from app.main import app  # noqa: E402


@pytest.fixture(autouse=True)
def banco_limpo():
    """
    Roda antes de CADA teste: apaga e recria todas as tabelas.
    Assim um teste nunca depende do que outro deixou gravado.
    """
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    yield


@pytest.fixture(scope="session", autouse=True)
def remover_banco_de_teste():
    """Ao final de toda a execucao, apaga o arquivo do banco de teste."""
    yield
    engine.dispose()
    if os.path.exists("bulbe_test.db"):
        os.remove("bulbe_test.db")


@pytest.fixture
def client() -> TestClient:
    """Cliente HTTP que chama a API sem precisar subir o uvicorn."""
    return TestClient(app)


@pytest.fixture
def headers_auth(client: TestClient) -> dict:
    """Cadastra um usuario, faz login e devolve o cabecalho Authorization."""
    client.post(
        "/v1/auth/registrar",
        json={"nome": "Operadora Bulbe", "email": "operacao@bulbe.com.br", "senha": "solar12345"},
    )
    resposta = client.post(
        "/v1/auth/login",
        data={"username": "operacao@bulbe.com.br", "password": "solar12345"},
    )
    token = resposta.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def usina_valida() -> dict:
    return {
        "nome": "Usina Solar Uberlandia",
        "localizacao": "Uberlandia, MG",
        "capacidade_geracao_kwh": 5000,
    }
