# Dependências e ferramentas — sendit

## Backend Python

O projeto instala dependências via `requirements.txt`; não foi identificado Poetry, Pipenv ou outro lockfile Python.

| Pacote | Versão declarada | Uso/sinal |
|---|---:|---|
| Django | 6.0.7 | Framework web principal |
| dj-database-url | 3.1.2 | Configuração de banco via URL |
| django-ckeditor-5 | 0.2.20 | Editor rich text |
| django-cors-headers | 4.9.0 | CORS |
| django-debug-toolbar | 6.3.0 | Diagnóstico em desenvolvimento |
| django-js-asset | 3.1.2 | Assets do ecossistema Django |
| django-mini-system-monitor | 0.3 | Monitor administrativo |
| django-miniexplorer | 0.6.1 | Exploração administrativa |
| django-request | 1.7.1 | Registro/inspeção de requisições |
| django-rq | 4.1.0 | Integração Django com RQ |
| django-session-security | 2.6.8 | Segurança/expiração de sessão |
| django-storages[s3] | 1.14.6 | Armazenamento S3 |
| gunicorn | 26.0.0 | Servidor WSGI |
| psycopg[binary] | 3.3.4 | Driver PostgreSQL |
| python-decouple | 3.8 | Configuração por ambiente |
| whitenoise | 6.12.0 | Servir arquivos estáticos |
| humanize | 4.15.0 | Formatação legível |
| Pillow | 12.3.0 | Imagens |
| rq-scheduler | 0.14.0 | Agendamento de tarefas RQ |
| docker | 7.1.0 | API Docker para Python |

Ferramentas de desenvolvimento em `requirements.dev.txt`: `black`, `pylint`, `pylint_django`, `isort` (sem versões fixadas). `.python-version` também existe; a imagem principal usa `python:3.14.5-alpine3.23`.

## Serviço Node.js (`projects-api/`)

Gerenciador: npm; `package-lock.json` presente. Pacote `backend@1.0.0`, ES modules (`type: module`). Scripts: `start` (Node em `api/server.js`), `dev` (watch), `test` (Node test runner) e `seeds`.

Dependências declaradas: `@hono/node-server ^2.0.1`, `chokidar ^5.0.0`, `directory-tree ^3.6.0`, `dockerode ^5.0.0`, `hono ^4.12.16`, `nanoid ^5.1.11`, `tar-fs ^3.1.2`, `ws ^8.20.0`. Dev dependency: `@biomejs/biome ^2.4.13`.

Dockerfile do serviço baseado em imagem Node (detalhes em `projects-api/Dockerfile` e `projects-api/Dockerfile.dev`).

## Serviços locais

`docker-compose.yml` declara PostgreSQL (`postgres`), Redis (`redis`), MinIO (`minio/minio`), MinIO client (`minio/mc`), Mailpit (`axllent/mailpit`), web, worker, scheduler, VM de execução e API Node. As imagens de banco, Redis, MinIO e Mailpit não têm tag fixada no Compose.
