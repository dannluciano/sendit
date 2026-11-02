# Núcleo da plataforma, Requirements

> Esta unit descreve as responsabilidades compartilhadas do app `core`. Os fluxos completos de conta, questões, submissões e ranking são detalhados nas units filhas.

## Visão Geral

O núcleo oferece os conceitos compartilhados pela plataforma de desafios: conta/perfil, catálogo de questões, submissões, avaliação de código, XP, ranking e conquistas. Ele conecta a interface Django aos workers RQ e ao executor Docker. 🟢

## Responsabilidades

- Gerenciar entidades centrais e rotas do SendIT. 🟢
- Permitir que usuários autenticados descubram questões e consultem seus resultados. 🟢
- Registrar submissões e delegar sua execução assíncrona. 🟢
- Consolidar XP, ranking e conquistas. 🟢

## Regras de Negócio

- O catálogo distingue questões visíveis e invisíveis; a seleção normal/aleatória exclui questões invisíveis. 🟢
- Submissões têm UUID e status inicial `Waiting`; a avaliação é realizada por worker. 🟢
- O ranking soma XP de questões resolvidas e conquistas, calcula nível com teto 74 e exclui o grupo `Staff`. 🟢
- 🔴 Política completa de cadastro, recuperação de conta e papéis administrativos deve ser validada com responsáveis do produto.

## Requisitos Funcionais

| ID | Requisito | Prioridade | Critério de Aceite |
|----|-----------|-----------|-------------------|
| RF-01 | Expor as capacidades de conta, questões, submissões, ranking e conquistas por meio dos apps/views do núcleo. 🟢 | Must | Rotas principais do `core.urls` respondem conforme autenticação e recurso solicitado. |
| RF-02 | Persistir submissões identificáveis por UUID e delegar processamento ao worker. 🟢 | Must | Uma submissão válida fica persistida em `Waiting` e é enfileirada uma vez. |
| RF-03 | Derivar páginas de questões pendentes, concluídas e ranking a partir de dados do usuário. 🟢 | Should | Usuário vê apenas estado e resultados correspondentes aos filtros de conta/grupo. |
| RF-04 | Exibir mensagens e imagens contextualizadas para resultados de submissão. 🟢 | Could | Para status conhecido, texto e imagem vêm do conjunto correspondente. |

## Requisitos Não Funcionais

| Tipo | Requisito inferido | Evidência no código | Confiança |
|------|--------------------|---------------------|-----------|
| Segurança | Rotas principais exigem sessão autenticada; detalhes de submissão permitem acesso do autor ou staff. | `core/views.py` (`login_required`, `submission_detail`) | 🟢 |
| Escalabilidade | Processamento de submissões passa por RQ/Redis em vez de bloquear a requisição web. | `core/views.py:create_submission`, `core/worker.py` | 🟢 |
| Disponibilidade | Execução de código isolada em container tem limites de CPU, memória, PIDs e timeout. | `core/submission_runner.py:SubmissionRunner.run_process` | 🟢 |

## Critérios de Aceitação

```gherkin
# 🟢 Fluxo principal de acesso às capacidades autenticadas
Dado um usuário com sessão válida
Quando ele abre a página inicial do núcleo
Então o sistema apresenta questões disponíveis e dados pessoais

# 🟢 Falha de acesso
Dado um visitante sem sessão
Quando ele solicita uma página protegida do núcleo
Então o sistema o encaminha para o fluxo de login

# 🟢 Fluxo principal de submissão
Dado um usuário autenticado sem submissão correta para a questão e sem tentativa nos últimos 15 segundos
Quando ele envia código e linguagem por POST
Então o sistema persiste uma submissão Waiting, agenda o worker e redireciona para seu status

# 🟢 Falha de reenvio
Dado um usuário com submissão correta da questão ou tentativa nos últimos 15 segundos
Quando ele envia outra submissão
Então o sistema redireciona para a questão sem criar nova submissão nem enfileirar trabalho
```

## Prioridade (MoSCoW)

| Requisito | MoSCoW | Justificativa |
|-----------|--------|---------------|
| Registro e processamento de submissões | Must | Caminho central e integrado ao worker. 🟢 |
| Catálogo de questões para usuários | Must | Entrada principal dos fluxos de aprendizagem. 🟡 |
| Ranking e conquistas | Should | Funcionalidades de progressão que não impedem executar questões. 🟢 |
| Textos/imagens randômicos de status | Could | Camada de apresentação sem efeito no resultado da avaliação. 🟡 |

> Prioridade inferida por frequência de chamada e posição na cadeia de dependências.

## Rastreabilidade de Código

| Arquivo | Função / Classe | Cobertura |
|---------|-----------------|-----------|
| `core/urls.py` | Rotas do núcleo | 🟢 |
| `core/models.py` | `Question`, `Submission`, `Achievement`, `UserData` | 🟢 |
| `core/views.py` | Páginas de questões, submissões e ranking | 🟢 |
| `core/domain.py` | Regras de ranking, perfil e seleção de questões | 🟢 |
| `core/worker.py` | `run_submission_runner` | 🟢 |
| `core/submission_runner.py` | Runner por linguagem | 🟢 |
| `core/admin.py` | Administração de conteúdo e usuários | 🟢 |
