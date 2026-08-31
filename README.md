# Helpdesk API

API RESTful para **Gestão de Chamados de TI**, desenvolvida em Flask, com persistência em banco relacional (SQLite por padrão, MySQL opcional), ORM via Flask-SQLAlchemy, migrações com Flask-Migrate e validação de payload com Marshmallow.

## Sumário

- [Domínio](#domínio)
- [Arquitetura](#arquitetura)
- [Pré-requisitos](#pré-requisitos)
- [Passo a passo para executar o projeto](#passo-a-passo-para-executar-o-projeto)
- [Testando a API pelo Postman](#testando-a-api-pelo-postman)
- [Tratamento de erros](#tratamento-de-erros)
- [Resetar o banco de dados](#resetar-o-banco-de-dados)
- [Problemas comuns](#problemas-comuns)

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
- [Postman](https://www.postman.com/downloads/) instalado (usado nos exemplos abaixo; Insomnia ou `curl` também funcionam)

## Passo a passo para executar o projeto

Siga **nessa ordem**. Cada passo depende do anterior.

### 1. Baixar o projeto

```bash
git clone https://github.com/odairoliv/help-desk.git
cd help-desk
```

### 2. Criar e ativar o ambiente virtual

**Windows (PowerShell):**

```bash
python -m venv .venv
.venv\Scripts\Activate.ps1
```

> Se o PowerShell bloquear a ativação com um erro de política de execução, rode antes: `Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned`

**Windows (CMD):**

```bash
python -m venv .venv
.venv\Scripts\activate.bat
```

**Linux/macOS:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Quando ativado, o prompt do terminal passa a exibir `(.venv)` no início da linha. **Todos os comandos seguintes assumem o ambiente virtual ativado.**

### 3. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 4. Configurar variáveis de ambiente

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

### 5. Criar o banco de dados (migrações)

A pasta `migrations/` já vem pronta no repositório, então basta aplicar o que já existe:

```bash
flask db upgrade
```

> ⚠️ **Este passo é obrigatório e não pode ser pulado.** O arquivo `helpdesk.db` não vem no Git (está no `.gitignore`) — sem rodar `flask db upgrade`, as tabelas não existem e qualquer chamada à API retorna `500 Internal Server Error` com `{"error": "Erro interno no servidor"}`. Sempre que clonar o projeto em uma pasta/máquina nova, ou apagar o `helpdesk.db`, rode este comando de novo antes de usar a API.

Só é necessário recriar as migrações do zero (`flask db init` + `flask db migrate`) se você alterar algum modelo em `app/models/`. Nesse caso:

```bash
flask db migrate -m "descricao da mudanca"
flask db upgrade
```

### 6. Rodar a API

```bash
python run.py
```

Saída esperada:

```
* Running on http://127.0.0.1:5000
```

A API está no ar em **`http://127.0.0.1:5000`**. Deixe esse terminal aberto — é nele que aparecem os logs e eventuais erros enquanto você usa a API.

### 7. Testar no Postman

Abra o Postman e siga a seção [Testando a API pelo Postman](#testando-a-api-pelo-postman) abaixo.

## Testando a API pelo Postman

Não é preciso importar nenhuma coleção — é só criar uma nova aba de requisição no Postman (`+`) e preencher método, URL e corpo conforme cada exemplo.

Estrutura de cada requisição no Postman:
1. Escolha o **método** (GET, POST, PUT, PATCH ou DELETE) no dropdown à esquerda da barra de URL.
2. Cole a **URL** no campo ao lado.
3. Quando houver corpo (POST/PUT/PATCH): clique na aba **Body** → marque **raw** → mude o tipo de `Text` para **JSON** (dropdown à direita) → cole o JSON do exemplo.
4. Clique em **Send**.

> **Ordem recomendada:** crie primeiro um Departamento, depois um Chamado (que referencia o `id` do departamento), depois um Comentário (que referencia o `id` do chamado). É a ordem usada nos exemplos abaixo.

### Departamentos

| Método | URL                                    | Descrição                                     |
|--------|-----------------------------------------|------------------------------------------------|
| GET    | `http://127.0.0.1:5000/departamentos`  | Lista departamentos (aceita `?nome=`, `?page=`, `?per_page=` na aba **Params**) |
| GET    | `http://127.0.0.1:5000/departamentos/1`| Consulta o departamento de id 1                |
| POST   | `http://127.0.0.1:5000/departamentos`  | Cria um novo departamento                      |
| PUT    | `http://127.0.0.1:5000/departamentos/1`| Atualiza **todos** os campos do departamento 1 |
| PATCH  | `http://127.0.0.1:5000/departamentos/1`| Atualiza **apenas** os campos enviados         |
| DELETE | `http://127.0.0.1:5000/departamentos/1`| Remove o departamento 1 (e seus chamados)      |

**1. Criar um departamento**
- Método: `POST` — URL: `http://127.0.0.1:5000/departamentos`
- Body → raw → JSON:
  ```json
  { "nome": "Infraestrutura", "responsavel": "Maria Silva" }
  ```
- Resposta esperada (`201 Created`):
  ```json
  { "id": 1, "nome": "Infraestrutura", "responsavel": "Maria Silva" }
  ```

**2. Listar departamentos**
- Método: `GET` — URL: `http://127.0.0.1:5000/departamentos`
- Para filtrar/paginar, use a aba **Params** do Postman e adicione as chaves `nome`, `page` ou `per_page` (ex.: `nome` = `infra`).

**3. Consultar um departamento pelo id**
- Método: `GET` — URL: `http://127.0.0.1:5000/departamentos/1`

**4. Atualizar totalmente (PUT — precisa enviar todos os campos)**
- Método: `PUT` — URL: `http://127.0.0.1:5000/departamentos/1`
- Body → raw → JSON:
  ```json
  { "nome": "Infraestrutura TI", "responsavel": "Maria Silva" }
  ```

**5. Atualizar parcialmente (PATCH — só o que for enviado é alterado)**
- Método: `PATCH` — URL: `http://127.0.0.1:5000/departamentos/1`
- Body → raw → JSON:
  ```json
  { "responsavel": "João Souza" }
  ```

**6. Remover**
- Método: `DELETE` — URL: `http://127.0.0.1:5000/departamentos/1`
- Resposta esperada: `204 No Content` (corpo vazio).

### Chamados

| Método | URL                                | Descrição                                                                 |
|--------|-------------------------------------|-----------------------------------------------------------------------------|
| GET    | `http://127.0.0.1:5000/chamados`   | Lista chamados (aceita `?status=`, `?prioridade=`, `?departamento_id=`, `?page=`, `?per_page=` na aba **Params**) |
| GET    | `http://127.0.0.1:5000/chamados/1` | Consulta o chamado de id 1                                                  |
| POST   | `http://127.0.0.1:5000/chamados`   | Cria um novo chamado                                                        |
| PUT    | `http://127.0.0.1:5000/chamados/1` | Atualiza **todos** os campos do chamado 1                                   |
| PATCH  | `http://127.0.0.1:5000/chamados/1` | Atualiza **apenas** os campos enviados                                      |
| DELETE | `http://127.0.0.1:5000/chamados/1` | Remove o chamado 1                                                          |

**1. Criar um chamado** (o `departamento_id` precisa existir — use o id criado no passo anterior)
- Método: `POST` — URL: `http://127.0.0.1:5000/chamados`
- Body → raw → JSON:
  ```json
  {
    "titulo": "Impressora não funciona",
    "descricao": "Impressora do 2º andar não liga",
    "prioridade": "media",
    "departamento_id": 1
  }
  ```
- Resposta esperada (`201 Created`):
  ```json
  {
    "id": 1,
    "titulo": "Impressora não funciona",
    "descricao": "Impressora do 2º andar não liga",
    "prioridade": "media",
    "status": "aberto",
    "departamento_id": 1,
    "criado_em": "2026-08-29T00:04:15.481043",
    "comentarios": []
  }
  ```
- Se o `departamento_id` não existir, a resposta é `400 Bad Request`.

**2. Listar chamados (com filtros)**
- Método: `GET` — URL: `http://127.0.0.1:5000/chamados`
- Na aba **Params**, adicione por exemplo `status` = `aberto` e `departamento_id` = `1`.

**3. Consultar um chamado pelo id**
- Método: `GET` — URL: `http://127.0.0.1:5000/chamados/1`
- A resposta já inclui o array `comentarios` com o histórico do chamado.

**4. Atualizar totalmente (PUT)**
- Método: `PUT` — URL: `http://127.0.0.1:5000/chamados/1`
- Body → raw → JSON:
  ```json
  {
    "titulo": "Impressora não funciona",
    "descricao": "Ainda sem solução",
    "prioridade": "alta",
    "status": "em_andamento",
    "departamento_id": 1
  }
  ```

**5. Atualizar só o status (PATCH)**
- Método: `PATCH` — URL: `http://127.0.0.1:5000/chamados/1`
- Body → raw → JSON:
  ```json
  { "status": "resolvido" }
  ```

**6. Remover**
- Método: `DELETE` — URL: `http://127.0.0.1:5000/chamados/1`
- Resposta esperada: `204 No Content`.

### Comentários

Comentários registram o histórico de atendimento de um chamado (ex.: atualizações de um técnico). Não têm PUT/PATCH — são um registro imutável: só são criados, listados e removidos.

| Método | URL                                                          | Descrição                              |
|--------|---------------------------------------------------------------|------------------------------------------|
| GET    | `http://127.0.0.1:5000/chamados/1/comentarios`                | Lista os comentários do chamado 1        |
| POST   | `http://127.0.0.1:5000/chamados/1/comentarios`                | Adiciona um comentário ao chamado 1      |
| DELETE | `http://127.0.0.1:5000/chamados/1/comentarios/1`               | Remove o comentário de id 1              |

**1. Adicionar um comentário** (o chamado `1` precisa existir)
- Método: `POST` — URL: `http://127.0.0.1:5000/chamados/1/comentarios`
- Body → raw → JSON:
  ```json
  { "texto": "Verificado com o usuário, reiniciando a máquina", "autor": "Técnico João" }
  ```
- Resposta esperada (`201 Created`):
  ```json
  {
    "id": 1,
    "texto": "Verificado com o usuário, reiniciando a máquina",
    "autor": "Técnico João",
    "chamado_id": 1,
    "criado_em": "2026-08-29T00:12:29.091913"
  }
  ```

**2. Listar comentários de um chamado**
- Método: `GET` — URL: `http://127.0.0.1:5000/chamados/1/comentarios`

**3. Remover um comentário**
- Método: `DELETE` — URL: `http://127.0.0.1:5000/chamados/1/comentarios/1`
- Resposta esperada: `204 No Content`.

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

Exemplo de erro de validação (`422`) no Postman, ao dar POST em `/departamentos` sem o campo `responsavel`:

```json
{
  "error": "Erro de validação",
  "detalhes": { "responsavel": ["Missing data for required field."] }
}
```

## Resetar o banco de dados

Para começar do zero (apaga todos os dados), com o servidor parado (`Ctrl+C` no terminal):

```bash
del helpdesk.db
flask db upgrade
```

*(no Linux/macOS use `rm helpdesk.db`)*

## Problemas comuns

**`{"error": "Erro interno no servidor"}` (500) logo na primeira chamada**
Faltou rodar `flask db upgrade` (passo 5). Pare o servidor, rode o comando e inicie de novo com `python run.py`.

**Postman retorna `ECONNREFUSED` ou "Could not send request"**
O servidor não está rodando, ou está rodando em outra porta/terminal. Confira o terminal onde rodou `python run.py` — ele precisa mostrar `Running on http://127.0.0.1:5000` e continuar aberto.

**`422 Unprocessable Entity` inesperado**
Confira se a aba **Body** do Postman está em **raw** com o tipo **JSON** selecionado (não `Text`), e se o JSON enviado é válido (aspas duplas, vírgulas corretas).

**Erro ao ativar o ambiente virtual no PowerShell**
Rode `Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned` antes de `.venv\Scripts\Activate.ps1`.
