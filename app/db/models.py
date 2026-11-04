"""
Modelos do SQLAlchemy: cada classe e uma tabela do banco.

Atencao: estes NAO sao os modelos do Dominio. Os modelos Pydantic de
app/domain continuam sendo o que a API recebe e devolve. Estes aqui
descrevem apenas como os dados ficam guardados.
"""

from datetime import date

from sqlalchemy import Date, Float, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class UsinaModel(Base):
    __tablename__ = "usinas"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(100))
    localizacao: Mapped[str] = mapped_column(String(100))
    capacidade_geracao_kwh: Mapped[float] = mapped_column(Float)
    status: Mapped[str] = mapped_column(String(20), default="ativa")
    data_ativacao: Mapped[date] = mapped_column(Date)


class UsuarioModel(Base):
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    senha_hash: Mapped[str] = mapped_column(String(100))
