"""
Camada de Persistencia, repositorios de Usina.

- UsinaRepository: o CONTRATO (interface). Diz quais metodos existem.
- InMemoryUsinaRepository: a versao em dicionario, usada nos testes unitarios.
- SqlUsinaRepository: a versao com banco de dados, usada pela API.

O UsinaService so conhece o contrato. Por isso ele nao muda.
"""

from datetime import date
from typing import Protocol

from sqlalchemy import select
from sqlalchemy.orm import Session, sessionmaker

from app.db.database import SessionLocal
from app.db.models import UsinaModel
from app.domain.usina import Usina, UsinaCreate, UsinaUpdate


class UsinaRepository(Protocol):
    def listar(self) -> list[Usina]: ...
    def buscar_por_id(self, usina_id: int) -> Usina | None: ...
    def criar(self, dados: UsinaCreate) -> Usina: ...
    def atualizar(self, usina_id: int, dados: UsinaUpdate) -> Usina | None: ...
    def remover(self, usina_id: int) -> bool: ...


class InMemoryUsinaRepository:
    """O mesmo repositorio do handson de CRUD, apenas renomeado."""

    def __init__(self) -> None:
        self._usinas: dict[int, Usina] = {}
        self._proximo_id: int = 1

    def listar(self) -> list[Usina]:
        return list(self._usinas.values())

    def buscar_por_id(self, usina_id: int) -> Usina | None:
        return self._usinas.get(usina_id)

    def criar(self, dados: UsinaCreate) -> Usina:
        usina = Usina(id=self._proximo_id, data_ativacao=date.today(), **dados.model_dump())
        self._usinas[usina.id] = usina
        self._proximo_id += 1
        return usina

    def atualizar(self, usina_id: int, dados: UsinaUpdate) -> Usina | None:
        usina_atual = self._usinas.get(usina_id)
        if usina_atual is None:
            return None
        dados_atualizados = usina_atual.model_dump()
        dados_atualizados.update(dados.model_dump(exclude_unset=True))
        usina_atualizada = Usina(**dados_atualizados)
        self._usinas[usina_id] = usina_atualizada
        return usina_atualizada

    def remover(self, usina_id: int) -> bool:
        if usina_id not in self._usinas:
            return False
        del self._usinas[usina_id]
        return True


class SqlUsinaRepository:
    """Mesmos metodos, agora lendo e gravando no banco com SQLAlchemy."""

    def __init__(self, session_factory: sessionmaker[Session]) -> None:
        self._session_factory = session_factory

    def listar(self) -> list[Usina]:
        with self._session_factory() as session:
            modelos = session.scalars(select(UsinaModel).order_by(UsinaModel.id)).all()
            return [Usina.model_validate(m) for m in modelos]

    def buscar_por_id(self, usina_id: int) -> Usina | None:
        with self._session_factory() as session:
            modelo = session.get(UsinaModel, usina_id)
            return Usina.model_validate(modelo) if modelo else None

    def criar(self, dados: UsinaCreate) -> Usina:
        with self._session_factory() as session:
            # mode="json" converte o enum StatusUsina no texto "ativa"
            modelo = UsinaModel(**dados.model_dump(mode="json"), data_ativacao=date.today())
            session.add(modelo)
            session.commit()
            session.refresh(modelo)  # traz o id gerado pelo banco
            return Usina.model_validate(modelo)

    def atualizar(self, usina_id: int, dados: UsinaUpdate) -> Usina | None:
        with self._session_factory() as session:
            modelo = session.get(UsinaModel, usina_id)
            if modelo is None:
                return None
            for campo, valor in dados.model_dump(mode="json", exclude_unset=True).items():
                setattr(modelo, campo, valor)
            session.commit()
            session.refresh(modelo)
            return Usina.model_validate(modelo)

    def remover(self, usina_id: int) -> bool:
        with self._session_factory() as session:
            modelo = session.get(UsinaModel, usina_id)
            if modelo is None:
                return False
            session.delete(modelo)
            session.commit()
            return True


# A instancia usada pela aplicacao agora fala com o banco.
usina_repository: UsinaRepository = SqlUsinaRepository(SessionLocal)
