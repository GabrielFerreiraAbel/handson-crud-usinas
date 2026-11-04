"""
Conexao com o banco de dados.

- engine: o "cano" ate o banco. Existe um so por aplicacao.
- SessionLocal: fabrica de sessoes. Cada operacao abre a sua sessao.
- Base: classe-mae de todos os modelos (tabelas).
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.core.config import DATABASE_URL

# O SQLite, por padrao, so aceita a conexao na thread que a criou.
# O FastAPI usa varias threads, entao liberamos essa checagem.
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args)

SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


class Base(DeclarativeBase):
    pass
