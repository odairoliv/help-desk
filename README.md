# Helpdesk API

API RESTful para Gestão de Chamados de TI, desenvolvida em Flask.

## Domínio

- **Departamento** (1) → **Chamado** (N)
- `Departamento`: `id`, `nome`, `responsavel`
- `Chamado`: `id`, `titulo`, `descricao`, `prioridade` (`baixa`, `media`, `alta`), `status` (`aberto`, `em_andamento`, `resolvido`), `departamento_id`, `criado_em`

## Arquitetura

```
app/
├── models/     # Entidades SQLAlchemy
├── schemas/    # Validação de payload (Marshmallow)
├── services/   # Regras de negócio / acesso a dados
└── routes/     # Blueprints (controladores HTTP)
```

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

Ajuste o `.env` se desejar usar MySQL (ex.: `DATABASE_URL=mysql+pymysql://usuario:senha@localhost/helpdesk`).

## Migrações do banco

```bash
flask db init
flask db migrate -m "estrutura inicial"
flask db upgrade
```

## Executar

```bash
python run.py
```

A API sobe em `http://127.0.0.1:5000`.

## Endpoints

### Departamentos

| Método | Rota                       | Descrição                          |
|--------|----------------------------|-------------------------------------|
| GET    | `/departamentos`           | Lista (filtros: `nome`, `page`, `per_page`) |
| GET    | `/departamentos/<id>`      | Detalha um departamento             |
| POST   | `/departamentos`           | Cria um departamento                |
| PUT    | `/departamentos/<id>`      | Atualiza completamente              |
| PATCH  | `/departamentos/<id>`      | Atualiza parcialmente               |
| DELETE | `/departamentos/<id>`      | Remove                              |

### Chamados

| Método | Rota                  | Descrição                                                        |
|--------|-----------------------|-------------------------------------------------------------------|
| GET    | `/chamados`           | Lista (filtros: `status`, `prioridade`, `departamento_id`, `page`, `per_page`) |
| GET    | `/chamados/<id>`      | Detalha um chamado                                                |
| POST   | `/chamados`           | Cria um chamado                                                   |
| PUT    | `/chamados/<id>`      | Atualiza completamente                                            |
| PATCH  | `/chamados/<id>`      | Atualiza parcialmente                                             |
| DELETE | `/chamados/<id>`      | Remove                                                            |

## Exemplo de payload

```json
POST /departamentos
{
  "nome": "Infraestrutura",
  "responsavel": "Maria Silva"
}
```

```json
POST /chamados
{
  "titulo": "Impressora não funciona",
  "descricao": "Impressora do 2º andar não liga",
  "prioridade": "media",
  "status": "aberto",
  "departamento_id": 1
}
```

## Tratamento de erros

Todas as respostas de erro seguem o formato:

```json
{ "error": "Mensagem descritiva" }
```

Códigos utilizados: `200`, `201`, `204`, `400`, `404`, `422`, `500`.
