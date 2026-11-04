"""
Configuracoes da aplicacao.

Em producao, chave secreta e endereco do banco NUNCA ficam no codigo:
eles vem de variaveis de ambiente. Os valores padrao servem para a aula.
"""

import os

SECRET_KEY: str = os.getenv("BULBE_SECRET_KEY", "troque-esta-chave-em-producao-bulbe-2026")
ALGORITHM: str = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("BULBE_TOKEN_MINUTOS", "30"))

# SQLite em arquivo local por padrao. Para PostgreSQL, por exemplo:
# postgresql+psycopg://bulbe:bulbe@localhost:5432/bulbe
DATABASE_URL: str = os.getenv("BULBE_DATABASE_URL", "sqlite:///./bulbe.db")
