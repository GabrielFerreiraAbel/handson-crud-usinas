"""
Testes de integracao dos repositorios SQL.
Usam o banco de teste de verdade, preparado pela fixture banco_limpo.
"""

from app.db.database import SessionLocal
from app.domain.usina import StatusUsina, UsinaCreate, UsinaUpdate
from app.repositories.usina_repository import SqlUsinaRepository
from app.repositories.usuario_repository import SqlUsuarioRepository


def nova_usina(nome: str = "Usina Solar Janauba") -> UsinaCreate:
    return UsinaCreate(nome=nome, localizacao="Janauba, MG", capacidade_geracao_kwh=7800)


def test_criar_grava_e_o_banco_gera_o_id():
    repo = SqlUsinaRepository(SessionLocal)
    usina = repo.criar(nova_usina())
    assert usina.id == 1
    assert usina.status == StatusUsina.ativa


def test_dado_persiste_entre_instancias_do_repositorio():
    # Duas instancias diferentes enxergam o mesmo dado: ele esta no banco,
    # nao na memoria do objeto.
    SqlUsinaRepository(SessionLocal).criar(nova_usina())
    outra_instancia = SqlUsinaRepository(SessionLocal)
    assert len(outra_instancia.listar()) == 1


def test_atualizar_status_no_banco():
    repo = SqlUsinaRepository(SessionLocal)
    usina = repo.criar(nova_usina())
    repo.atualizar(usina.id, UsinaUpdate(status=StatusUsina.em_manutencao))
    assert repo.buscar_por_id(usina.id).status == StatusUsina.em_manutencao


def test_remover_apaga_do_banco():
    repo = SqlUsinaRepository(SessionLocal)
    usina = repo.criar(nova_usina())
    assert repo.remover(usina.id) is True
    assert repo.buscar_por_id(usina.id) is None
    assert repo.remover(usina.id) is False


def test_usuario_e_buscado_pelo_email_sem_diferenciar_maiusculas():
    repo = SqlUsuarioRepository(SessionLocal)
    repo.criar("Operadora Bulbe", "Operacao@Bulbe.com.br", "hash-qualquer")
    assert repo.buscar_por_email("operacao@bulbe.com.br").nome == "Operadora Bulbe"
