# Software Sales API

API REST para cadastro de usuários, cursos, avaliações, compras e auditoria. O projeto usa Django 4.2, Django REST Framework, JWT, PostgreSQL e Docker.

## Recursos

- Cadastro e autenticação JWT com refresh token.
- CRUD de cursos com controle de propriedade.
- Avaliações únicas por usuário e curso.
- Compras isoladas por usuário.
- Métricas de vendas concluídas e média das avaliações.
- Auditoria de compras e avaliações acessível somente a administradores.
- Swagger em `/swagger/` e ReDoc em `/redoc/`.

## Configuração

Copie o arquivo de exemplo e substitua todos os valores marcados para troca:

```powershell
Copy-Item .env.example .env
```

Em Linux/macOS:

```sh
cp .env.example .env
```

Nunca versione `.env`, senhas ou tokens reais.

## Executar com Docker

Desenvolvimento com recarga automática:

```sh
docker compose -f docker-compose.yml -f docker-compose.dev.yml up --build
```

Configuração de produção local:

```sh
docker compose -f docker-compose.yml -f docker-compose.prod.yml up --build -d
```

A API fica disponível em `http://localhost:8000/`. O entrypoint aplica migrations e coleta arquivos estáticos antes de iniciar o servidor.

## Executar sem Docker

Requer Python 3.12 e PostgreSQL, ou ausência de `DATABASE_URL` para usar SQLite em desenvolvimento.

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Validação

```sh
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py test -v 2
python manage.py collectstatic --noinput
```

Para revisar configurações de produção:

```sh
DEBUG=False python manage.py check --deploy
```

Não há frontend neste repositório. Os endpoints podem ser consumidos por qualquer cliente HTTP usando `Authorization: Bearer <access_token>`.

## Autor

**Orlando Conceição Vilhalba de Almeida**

Desenvolvedor Backend em formação, com foco em Python, Django, Django REST Framework, PostgreSQL, APIs REST e Docker, utilizando React como tecnologia complementar para integração das aplicações.

GitHub: https://github.com/orlandoconceicao

LinkedIn: https://www.linkedin.com/in/orlando-concei%C3%A7%C3%A3o-582234315

Portfólio: https://orlandoconceicao.github.io/
