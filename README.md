# Handson: CRUD de Usinas em FastAPI

CRUD completo da entidade **Usina** (fazenda solar da Bulbe Energia), implementado com arquitetura em camadas: Apresentação, Serviço, Domínio e Persistência.

- **Disciplina:** Projeto Ciência de Dados II, Ibmec, 2º semestre de 2026
- **Professor:** Cristiano de Macedo Neto, M.Sc.
- **Aula:** 09, arquitetura em camadas
- **Equipe:** Squad Silver Lake
- **Empresa parceira:** Bulbe Energia (bulbeenergia.com.br)

A persistência usa uma base em memória. Quando o banco relacional entrar (Aula 19), apenas a camada `repositories/` muda; o restante do código permanece igual.

## Estrutura

```
handson-crud-usinas/
├── app/
│   ├── domain/
│   │   └── usina.py              formatos de entrada e saída, com validação Pydantic
│   ├── repositories/
│   │   └── usina_repository.py   única camada que sabe como os dados são guardados
│   ├── services/
│   │   └── usina_service.py      regras de negócio e erros padronizados
│   ├── controllers/
│   │   └── usina_controller.py   recebe a requisição HTTP e delega ao service
│   └── main.py                   monta o FastAPI e trata ErroDeNegocio
└── requirements.txt
```

## Como executar

```bash
python3 -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

A aplicação sobe em `http://localhost:8000`. O Swagger UI fica em `http://localhost:8000/docs`, onde é possível testar todos os endpoints pelo navegador.

## Endpoints

| Método | Rota | Descrição | Status |
|---|---|---|---|
| GET | `/v1/usinas` | Lista todas as usinas cadastradas | 200 |
| GET | `/v1/usinas/{id}` | Retorna uma usina específica | 200 / 404 |
| POST | `/v1/usinas` | Cria uma nova usina | 201 / 422 |
| PUT | `/v1/usinas/{id}` | Atualiza uma usina existente | 200 / 404 / 422 |
| DELETE | `/v1/usinas/{id}` | Remove uma usina | 204 / 404 |

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
- **Repository:** única camada que conhece o armazenamento. Hoje um dicionário em memória.

## Exercícios propostos

1. Endpoint `GET /v1/usinas/status/{status}` filtrando por status.
2. Regra de negócio no Service: só remover usina com status `inativa`, caso contrário `ErroDeNegocio` com `code="REMOCAO_NAO_PERMITIDA"` e `status=409`.
3. Padronizar os erros de validação do Pydantic no mesmo formato `error.code/message/status`.
4. Diagrama de sequência em PlantUML da operação `POST /v1/usinas`.
