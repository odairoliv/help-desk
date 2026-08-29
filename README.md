# Helpdesk API

API RESTful para **Gestão de Chamados de TI**, desenvolvida em Flask, com persistência em banco relacional (SQLite por padrão, MySQL opcional), ORM via Flask-SQLAlchemy, migrações com Flask-Migrate e validação de payload com Marshmallow.

## Sumário

- [Domínio](#domínio)
- [Arquitetura](#arquitetura)
- [Pré-requisitos](#pré-requisitos)
- [1. Baixar o projeto](#1-baixar-o-projeto)
- [2. Criar e ativar o ambiente virtual](#2-criar-e-ativar-o-ambiente-virtual)
- [3. Instalar as dependências](#3-instalar-as-dependências)
- [4. Configurar variáveis de ambiente](#4-configurar-variáveis-de-ambiente)
- [5. Criar o banco de dados (migrações)](#5-criar-o-banco-de-dados-migrações)
- [6. Rodar a API](#6-rodar-a-api)
- [Como usar — endpoints e exemplos](#como-usar--endpoints-e-exemplos)
- [Tratamento de erros](#tratamento-de-erros)
- [Resetar o banco de dados](#resetar-o-banco-de-dados)

## Domínio

- **Departamento** (1) → **Chamado** (N): cada chamado pertence obrigatoriamente a um departamento.
- **Chamado** (1) → **Comentário** (N): cada chamado pode acumular vários comentários (histórico de atendimento).
- `Departamento`: `id`, `nome`, `responsavel`
- `Chamado`: `id`, `titulo`, `descricao`, `prioridade` (`baixa`, `media`, `alta`), `status` (`aberto`, `em_andamento`, `resolvido`), `departamento_id`, `criado_em`
- `Comentário`: `id`, `texto`, `autor`, `chamado_id`, `criado_em`

## Arquitetura

Código organizado em camadas, sem lógica de negócio nas rotas:

```
app/
├── models/     # Entidades SQLAlchemy (tabelas e relacionamentos)
├── schemas/    # Validação de payload de entrada/saída (Marshmallow)
├── services/   # Regras de negócio e acesso ao banco
├── routes/     # Blueprints — apenas recebem a requisição e devolvem a resposta
├── errors.py   # Exceções customizadas (NotFoundError, BadRequestError)
└── __init__.py # Application factory + tratamento global de erros
config.py       # Configuração (lê variáveis do .env)
run.py          # Ponto de entrada da aplicação
migrations/     # Histórico de migrações do banco (Alembic/Flask-Migrate)
```

## Pré-requisitos

- [Python 3.11+](https://www.python.org/downloads/) instalado e no `PATH` (`python --version`)
- [Git](https://git-scm.com/downloads)
- Opcional: um cliente HTTP para testar a API — [Postman](https://www.postman.com/downloads/), [Insomnia](https://insomnia.rest/download) ou `curl` (já vem no Windows 10/11, macOS e Linux)

## 1. Baixar o projeto

```bash
git clone https://github.com/odairoliv/help-desk.git
cd help-desk
```

## 2. Criar e ativar o ambiente virtual

**Windows (PowerShell ou CMD):**

```bash
python -m venv .venv
.venv\Scripts\activate
```

**Linux/macOS:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Quando ativado, o prompt do terminal passa a exibir `(.venv)` no início da linha.

## 3. Instalar as dependências

```bash
pip install -r requirements.txt
```

## 4. Configurar variáveis de ambiente

Copie o arquivo de exemplo:

```bash
copy .env.example .env
```

*(no Linux/macOS use `cp .env.example .env`)*

Por padrão o `.env` já vem configurado para usar **SQLite** (não precisa instalar nada extra):

```
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=change-me
DATABASE_URL=sqlite:///helpdesk.db
```

Se preferir **MySQL**, instale o driver e troque a `DATABASE_URL`:

```bash
pip install pymysql
```

```
DATABASE_URL=mysql+pymysql://usuario:senha@localhost/helpdesk
```

## 5. Criar o banco de dados (migrações)

Com o ambiente virtual ativado, rode:

```bash
flask db init
flask db migrate -m "estrutura inicial"
flask db upgrade
```

- `flask db init` — cria a pasta `migrations/` (só é necessário rodar uma vez; se ela já existir no repositório, pule este passo).
- `flask db migrate` — gera o script de migração a partir dos modelos.
- `flask db upgrade` — aplica a migração e cria as tabelas no banco.

Se a pasta `migrations/` já vier no repositório (é o caso deste projeto), basta rodar:

```bash
flask db upgrade
```

## 6. Rodar a API

```bash
python run.py
```

Saída esperada:

```
* Running on http://127.0.0.1:5000
```

A API está no ar em **`http://127.0.0.1:5000`**. Deixe esse terminal aberto enquanto for usar a API.

## Como usar — endpoints e exemplos

Todos os exemplos abaixo usam `curl`. Se preferir, importe as mesmas requisições no Postman/Insomnia trocando `curl` pelos campos de método/URL/body.

### Departamentos

| Método | Rota                     | Descrição                                     |
|--------|--------------------------|------------------------------------------------|
| GET    | `/departamentos`         | Lista departamentos (filtros: `nome`, `page`, `per_page`) |
| GET    | `/departamentos/<id>`    | Consulta um departamento pelo id               |
| POST   | `/departamentos`         | Cria um novo departamento                      |
| PUT    | `/departamentos/<id>`    | Atualiza **todos** os campos do departamento   |
| PATCH  | `/departamentos/<id>`    | Atualiza **apenas** os campos enviados         |
| DELETE | `/departamentos/<id>`    | Remove o departamento (e seus chamados)        |

**Criar um departamento:**

```bash
curl -X POST http://127.0.0.1:5000/departamentos \
  -H "Content-Type: application/json" \
  -d "{\"nome\": \"Infraestrutura\", \"responsavel\": \"Maria Silva\"}"
```

Resposta (`201 Created`):

```json
{ "id": 1, "nome": "Infraestrutura", "responsavel": "Maria Silva" }
```

**Listar departamentos (com filtro e paginação):**

```bash
curl "http://127.0.0.1:5000/departamentos?nome=infra&page=1&per_page=10"
```

**Consultar um departamento:**

```bash
curl http://127.0.0.1:5000/departamentos/1
```

**Atualizar totalmente (PUT — precisa enviar todos os campos):**

```bash
curl -X PUT http://127.0.0.1:5000/departamentos/1 \
  -H "Content-Type: application/json" \
  -d "{\"nome\": \"Infraestrutura TI\", \"responsavel\": \"Maria Silva\"}"
```

**Atualizar parcialmente (PATCH — só o que for enviado é alterado):**

```bash
curl -X PATCH http://127.0.0.1:5000/departamentos/1 \
  -H "Content-Type: application/json" \
  -d "{\"responsavel\": \"João Souza\"}"
```

**Remover:**

```bash
curl -X DELETE http://127.0.0.1:5000/departamentos/1
```

Resposta: `204 No Content` (sem corpo).

### Chamados

| Método | Rota                | Descrição                                                                 |
|--------|---------------------|----------------------------------------------------------------------------|
| GET    | `/chamados`         | Lista chamados (filtros: `status`, `prioridade`, `departamento_id`, `page`, `per_page`) |
| GET    | `/chamados/<id>`    | Consulta um chamado pelo id                                                |
| POST   | `/chamados`         | Cria um novo chamado                                                       |
| PUT    | `/chamados/<id>`    | Atualiza **todos** os campos do chamado                                    |
| PATCH  | `/chamados/<id>`    | Atualiza **apenas** os campos enviados                                     |
| DELETE | `/chamados/<id>`    | Remove o chamado                                                           |

**Criar um chamado** (`departamento_id` precisa existir):

```bash
curl -X POST http://127.0.0.1:5000/chamados \
  -H "Content-Type: application/json" \
  -d "{\"titulo\": \"Impressora não funciona\", \"descricao\": \"Impressora do 2º andar não liga\", \"prioridade\": \"media\", \"departamento_id\": 1}"
```

Resposta (`201 Created`):

```json
{
  "id": 1,
  "titulo": "Impressora não funciona",
  "descricao": "Impressora do 2º andar não liga",
  "prioridade": "media",
  "status": "aberto",
  "departamento_id": 1,
  "criado_em": "2026-08-29T00:04:15.481043"
}
```

**Listar chamados filtrando por status e departamento:**

```bash
curl "http://127.0.0.1:5000/chamados?status=aberto&departamento_id=1"
```

**Consultar um chamado:**

```bash
curl http://127.0.0.1:5000/chamados/1
```

**Atualizar totalmente (PUT):**

```bash
curl -X PUT http://127.0.0.1:5000/chamados/1 \
  -H "Content-Type: application/json" \
  -d "{\"titulo\": \"Impressora não funciona\", \"descricao\": \"Ainda sem solução\", \"prioridade\": \"alta\", \"status\": \"em_andamento\", \"departamento_id\": 1}"
```

**Atualizar só o status (PATCH):**

```bash
curl -X PATCH http://127.0.0.1:5000/chamados/1 \
  -H "Content-Type: application/json" \
  -d "{\"status\": \"resolvido\"}"
```

**Remover:**

```bash
curl -X DELETE http://127.0.0.1:5000/chamados/1
```

> `GET /chamados/<id>` (e a listagem) já retorna o campo `comentarios` aninhado com o histórico do chamado.

### Comentários

Comentários registram o histórico de atendimento de um chamado (ex.: atualizações de um técnico). Não têm PUT/PATCH — são um registro imutável, apenas criados e removidos.

| Método | Rota                                          | Descrição                              |
|--------|------------------------------------------------|------------------------------------------|
| GET    | `/chamados/<chamado_id>/comentarios`           | Lista os comentários de um chamado       |
| POST   | `/chamados/<chamado_id>/comentarios`           | Adiciona um comentário ao chamado        |
| DELETE | `/chamados/<chamado_id>/comentarios/<id>`      | Remove um comentário                     |

**Adicionar um comentário:**

```bash
curl -X POST http://127.0.0.1:5000/chamados/1/comentarios \
  -H "Content-Type: application/json" \
  -d "{\"texto\": \"Verificado com o usuário, reiniciando a máquina\", \"autor\": \"Técnico João\"}"
```

Resposta (`201 Created`):

```json
{
  "id": 1,
  "texto": "Verificado com o usuário, reiniciando a máquina",
  "autor": "Técnico João",
  "chamado_id": 1,
  "criado_em": "2026-08-29T00:12:29.091913"
}
```

**Listar comentários de um chamado:**

```bash
curl http://127.0.0.1:5000/chamados/1/comentarios
```

**Remover um comentário:**

```bash
curl -X DELETE http://127.0.0.1:5000/chamados/1/comentarios/1
```

## Tratamento de erros

Todas as respostas de erro seguem o mesmo formato:

```json
{ "error": "Mensagem descritiva" }
```

| Código | Quando acontece                                                        |
|--------|--------------------------------------------------------------------------|
| 200    | Consulta (GET) ou atualização (PUT/PATCH) com sucesso                    |
| 201    | Criação (POST) com sucesso                                               |
| 204    | Remoção (DELETE) com sucesso, sem corpo de retorno                       |
| 400    | Requisição inválida (ex.: `departamento_id` de um chamado não existe)    |
| 404    | Recurso não encontrado (id inexistente)                                  |
| 422    | Erro de validação do payload (campo obrigatório faltando, tipo errado, valor fora da lista permitida) |
| 500    | Erro interno não previsto                                                |

Exemplo de erro de validação (`422`), ao criar um departamento sem o campo `responsavel`:

```json
{
  "error": "Erro de validação",
  "detalhes": { "responsavel": ["Missing data for required field."] }
}
```

## Resetar o banco de dados

Para começar do zero (apaga todos os dados), com o servidor parado:

```bash
del helpdesk.db
flask db upgrade
```

*(no Linux/macOS use `rm helpdesk.db`)*
