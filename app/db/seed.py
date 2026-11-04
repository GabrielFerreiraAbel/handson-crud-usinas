"""
Popula o banco com dados de exemplo da Bulbe Energia.
Uso:  python -m app.db.seed
Rode depois de "alembic upgrade head".
"""

from app.domain.usina import StatusUsina, UsinaCreate
from app.domain.usuario import UsuarioCreate
from app.repositories.usina_repository import usina_repository
from app.services.auth_service import auth_service
from app.services.usina_service import ErroDeNegocio

USINAS_EXEMPLO = [
    UsinaCreate(nome="Usina Solar Uberlandia", localizacao="Uberlandia, MG", capacidade_geracao_kwh=5000),
    UsinaCreate(nome="Usina Solar Montes Claros", localizacao="Montes Claros, MG", capacidade_geracao_kwh=3200),
    UsinaCreate(nome="Usina Solar Janauba", localizacao="Janauba, MG", capacidade_geracao_kwh=7800),
    UsinaCreate(
        nome="Usina Solar Sete Lagoas",
        localizacao="Sete Lagoas, MG",
        capacidade_geracao_kwh=1500,
        status=StatusUsina.em_manutencao,
    ),
]


def main() -> None:
    try:
        auth_service.registrar(
            UsuarioCreate(nome="Operadora Bulbe", email="operacao@bulbe.com.br", senha="solar12345")
        )
        print("Usuario operacao@bulbe.com.br criado (senha: solar12345)")
    except ErroDeNegocio:
        print("Usuario operacao@bulbe.com.br ja existia")

    if usina_repository.listar():
        print("Ja existem usinas cadastradas. Nada a fazer.")
        return
    for dados in USINAS_EXEMPLO:
        usina = usina_repository.criar(dados)
        print(f"Usina {usina.id}: {usina.nome}")


if __name__ == "__main__":
    main()
