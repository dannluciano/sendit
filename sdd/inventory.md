# Inventário do sistema — sendit

**Data do reconhecimento:** 2026-11-02  
**Nível de documentação configurado:** completo  
**Escopo:** reconhecimento inicial da superfície; comportamento e regras de negócio ficam para as próximas etapas.

## Visão geral

O SendIT é uma aplicação web para avaliações e execução de código. A estrutura contém um backend principal em Django/Python e um serviço auxiliar Node.js em `projects-api/`, responsável por operações do ambiente de projetos/IDE. O ambiente de desenvolvimento é orquestrado por Docker Compose.

## Linguagens

Contagem aproximada dos arquivos rastreados pelo Git por extensão: JavaScript (349), HTML (208), Python (83), CSS (106), SCSS (79), JSON (8), Markdown (7), shell (3), YAML (1), TOML (1), além de SVG, imagens, fontes e arquivos de configuração. O inventário inclui arquivos estáticos e templates; Python é a linguagem principal do backend e JavaScript domina a contagem geral por incluir recursos do frontend.

## Aplicações e módulos

- `core/` — núcleo da aplicação, contas, conteúdo, submissões, execução e funcionalidades gerais.
- `evaluation/` — avaliações e questões.
- `editor/` — editor/runner de código.
- `projects/` — interface web da IDE e projetos.
- `statistics/` — estatísticas, atividade e middleware.
- `projects-api/` — serviço Node.js separado para projetos, sessões de terminal e integração com containers.
- `SendIT/` — configuração Django, roteamento raiz e WSGI.

## Entradas e roteamento

- `manage.py` — comandos Django.
- `SendIT/wsgi.py` — entrada WSGI usada por Gunicorn.
- `SendIT/urls.py` — roteamento principal; inclui `core`, `evaluation`, `editor`, `projects`, `statistics`, admin, Django RQ e CKEditor.
- `projects-api/api/server.js` — entrada Node.js, configurada no script `start` do pacote.
- `projects-api/api/routes.js` e `projects-api/commands/routes.js` — arquivos de rotas do serviço auxiliar.

## Persistência e dados

O Django usa PostgreSQL via `DATABASE_URL` (padrão local apontando para o serviço `db`). Redis é usado para cache e filas RQ. Há migrações Django em `core/migrations/`, `editor/migrations/`, `evaluation/migrations/`, `projects/migrations/` e `statistics/migrations/`; fixtures em `core/fixtures/seed.json`. O serviço Node tem `projects-api/api/database.js`. O Compose também provisiona MinIO para armazenamento compatível com S3.

## Integrações e infraestrutura detectadas

- PostgreSQL: dados relacionais.
- Redis + django-rq/rq-scheduler: filas, workers e scheduler.
- AWS S3 compatível (django-storages) e MinIO local: arquivos e mídia.
- Docker/Dockerode: ambientes de execução de código e containers.
- SMTP: envio de e-mail configurável por variáveis de ambiente.
- WebSocket (`ws` no serviço Node): comunicação interativa do ambiente de projetos.
- Mailpit no Compose: captura local de e-mails.

## Configuração, execução e entrega

- Configuração principal: `SendIT/settings.py`, `env.sample`, `.env` (referenciado pelo Compose), `ruff.toml` e `gunicorn.conf.py`.
- CI/CD: nenhum workflow GitHub Actions, Jenkinsfile ou `.gitlab-ci.yml` apareceu no inventário superficial.
- Container principal: `Dockerfile`; desenvolvimento e dependências auxiliares em `Dockerfile.dev` e `docker-compose.yml`.
- Processos de produção descritos em `Procfile`: web, worker, scheduler e migração de release.
- `Makefile`: comandos para Docker Compose, logs e deploy.

## Testes

Há testes Django nos apps `core`, `evaluation`, `editor` e `projects`, além de `statistics/tests.py`. `projects-api/package.json` declara `node --test 'api/**/*.test.js'`; nenhum arquivo correspondente foi confirmado no inventário inicial. A cobertura não foi executada nem estimada por percentagem.

## Organização sugerida para as specs

**Híbrida.** O roteamento centralizado de Django e as rotas explícitas do serviço Node coexistem com apps de domínio separados (`core`, `evaluation`, `editor`, `projects`, `statistics`). Isso sugere organizar por módulo e destacar contratos/fluxos de endpoint quando relevante.

## Pontos para aprofundar

- Modelos e relacionamentos entre os apps Django e o banco Node.
- Fluxo completo de submissão e execução de código, incluindo isolamento e ciclo de vida dos containers.
- Contratos de API e WebSocket entre a aplicação Django, `projects-api` e os ambientes de execução.
- Configuração por ambiente para Redis, S3/MinIO, e-mail e banco.
- Testes automatizados existentes e cobertura real.
