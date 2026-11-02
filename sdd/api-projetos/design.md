# API de projetos, Design Técnico

## Interface

| Símbolo | Assinatura | Retorno | Observação |
|---|---|---|---|
| `projects-api/api/app.js:1` | API/worker/model conforme fonte | entidade, resposta ou evento | 🟢 |
| `projects-api/api/routes.js:9` | API/worker/model conforme fonte | entidade, resposta ou evento | 🟢 |
| `projects-api/api/auth/auth_middleware.js:5` | API/worker/model conforme fonte | entidade, resposta ou evento | 🟢 |

## Fluxo Principal

1. Boot conecta Docker e prepara imagem; /api verifica cookie assinado; create provisiona ComputerUnit e mapas locais registram estado. 🟢
2. Atualizar estado e devolver resultado ao consumidor. 🟢

## Fluxos Alternativos

- **Falha:** Falha Docker encerra processo; erro de criação retorna 500; upgrade websocket não usa middleware HTTP. 🟢 🟢
- **Divergência do legado:** middleware HTTP não cobre upgrade WebSocket. 🔴 Contrato alvo confirmado exige autenticação Django e autorização de owner em cada operação. 🟢

## Dependências

- Docker Engine/socket, Hono, Dockerode, ws, cookie Django 🟢

## Decisões de Design Identificadas

| Decisão | Evidência no código | Confiança |
|---|---|---|
| Preservar integração existente e serialização de estado. | `projects-api/api/app.js:1` | 🟢 |
| Aplicar limites e fluxo de recursos declarados. | `projects-api/api/routes.js:9` | 🟢 |

## Estado Interno

O serviço Node mantém associações de containers e WebSockets em `Map` de processo; o workspace fica no filesystem montado em volume do container. Não foi encontrado armazenamento persistente de estado da API em banco. 🟢

## Observabilidade

Erros são logados nas fontes citadas; métricas distribuídas não foram encontradas. 🟢

## Riscos e Lacunas

- Upgrade WebSocket exige autenticação Django e autorização por owner conforme política confirmada; legado diverge. 🟢

