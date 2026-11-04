# Handson: CRUD de Usinas em FastAPI

CRUD completo da entidade **Usina** (fazenda solar da Bulbe Energia), implementado com arquitetura em camadas: Apresentação, Serviço, Domínio e Persistência.

- **Disciplina:** Projeto Ciência de Dados II, Ibmec, 2º semestre de 2026
- **Professor:** Cristiano de Macedo Neto, M.Sc. 
- **Aulas:** 09 (arquitetura em camadas), 10 (JWT e testes unitários), 26 e 28 (banco de dados com SQLAlchemy e Alembic)
- **Equipe:** Squad Silver Lake 
- **Empresa parceira:** Bulbe Energia (bulbeenergia.com.br)

Os dados ficam em um banco relacional (SQLite por padrão, no arquivo `bulbe.db`), acessado com SQLAlchemy, e o schema é criado e versionado por migrations do Alembic. Na troca da memória para o banco, só a camada `repositories/` mudou: domínio, services, controllers e `main.py` ficaram iguais.

## Estrutura

```
handson-crud-usinas/
├── app/
│   ├── core/
│   │   ├── config.py               chave do JWT e endereço do banco
│   │   ├── security.py             hash bcrypt e geração/leitura do JWT
│   │   └── dependencies.py         obter_usuario_atual, o porteiro das rotas
│   ├── db/
│   │   ├── database.py             engine, SessionLocal e Base
│   │   ├── models.py               tabelas usinas e usuarios
│   │   └── seed.py                 dados de exemplo
│   ├── domain/
│   │   ├── usina.py                formatos de entrada e saída, com validação Pydantic
│   │   └── usuario.py
│   ├── repositories/
│   │   ├── usina_repository.py     contrato, versão em memória e versão SQL
│   │   └── usuario_repository.py
│   ├── services/
│   │   ├── usina_service.py        regras de negócio e erros padronizados
│   │   └── auth_service.py         cadastro, login e validação do token
│   ├── controllers/
│   │   ├── usina_controller.py     recebe a requisição HTTP e delega ao service
│   │   └── auth_controller.py
│   └── main.py                     monta o FastAPI e trata ErroDeNegocio
├── migrations/                     migrations do Alembic (env.py e versions/)
├── tests/                          testes unitários e de integração
├── alembic.ini
├── pytest.ini
└── requirements.txt
```

## Como executar

```bash
python3 -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
alembic upgrade head              # cria as tabelas no bulbe.db
python -m app.db.seed             # opcional: usuário e usinas de exemplo
uvicorn app.main:app --reload
```

A aplicação sobe em `http://localhost:8000`. O Swagger UI fica em `http://localhost:8000/docs`, onde é possível testar todos os endpoints pelo navegador. Para as rotas protegidas, clique em **Authorize** e entre com `operacao@bulbe.com.br` e `solar12345`, o usuário criado pelo seed.

O endereço do banco vem da variável `BULBE_DATABASE_URL`. Sem ela, o padrão é `sqlite:///./bulbe.db`. O `bulbe.db` fica fora do Git: cada pessoa gera o seu com `alembic upgrade head`.

## Como testar

```bash
pytest -v
```

São 33 testes. Os unitários rodam sem banco; os de integração usam um banco separado, `bulbe_test.db`, recriado a cada teste e apagado no final, nunca o `bulbe.db` de desenvolvimento.

## Endpoints

| Método | Rota | Descrição | Token | Status |
|---|---|---|---|---|
| POST | `/v1/auth/registrar` | Cadastra um usuário | não | 201 / 409 / 422 |
| POST | `/v1/auth/login` | Login por formulário, devolve o JWT | não | 200 / 401 |
| GET | `/v1/auth/me` | Devolve o usuário dono do token | sim | 200 / 401 |
| GET | `/v1/usinas` | Lista todas as usinas cadastradas | não | 200 |
| GET | `/v1/usinas/{id}` | Retorna uma usina específica | não | 200 / 404 |
| POST | `/v1/usinas` | Cria uma nova usina | sim | 201 / 401 / 422 |
| PUT | `/v1/usinas/{id}` | Atualiza uma usina existente | sim | 200 / 401 / 404 / 422 |
| DELETE | `/v1/usinas/{id}` | Remove uma usina | sim | 204 / 401 / 404 |

## Formato de erro

Erros de negócio são padronizados pelo handler em `main.py`:

```json
{
  "error": {
    "code": "RECURSO_NAO_ENCONTRADO",
    "message": "Usina com id 99 nao foi encontrada.",
    "status": 404
  }
}
```

Erros de validação do Pydantic ainda saem no formato padrão do FastAPI (`detail`), e não neste. Uniformizar os dois é um dos exercícios propostos.

## Responsabilidade de cada camada

- **Controller:** recebe a requisição, valida a entrada via Pydantic e formata a resposta. Não acessa dados nem decide regra de negócio.
- **Service:** concentra as regras e decide o que é erro de negócio, levantando `ErroDeNegocio` com `code`, `message` e `status`.
- **Domain:** define os formatos de entrada e saída, com validação automática. Independente de banco e de framework web.
- **Repository:** única camada que conhece o armazenamento. Cada repositório tem um contrato (`Protocol`) e duas implementações: em memória, usada nos testes unitários de service, e SQL, usada pela API.

## Exercícios propostos

1. Endpoint `GET /v1/usinas/status/{status}` filtrando por status.
2. Regra de negócio no Service: só remover usina com status `inativa`, caso contrário `ErroDeNegocio` com `code="REMOCAO_NAO_PERMITIDA"` e `status=409`.
3. Padronizar os erros de validação do Pydantic no mesmo formato `error.code/message/status`.
4. Diagrama de sequência em PlantUML da operação `POST /v1/usinas`.
