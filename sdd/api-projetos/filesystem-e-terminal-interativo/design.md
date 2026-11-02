# Filesystem e terminal interativo, Design Técnico

## Interface

| Símbolo | Assinatura | Retorno | Observação |
|---|---|---|---|
| `projects-api/api/websocket/api_websocket.js:6` | API/worker/model conforme fonte | entidade, resposta ou evento | 🟢 |
| `projects-api/api/websocket/docker_websocket.js:3` | API/worker/model conforme fonte | entidade, resposta ou evento | 🟢 |
| `projects-api/api/computer_unit/temp_dir.js:20` | API/worker/model conforme fonte | entidade, resposta ou evento | 🟢 |

## Fluxo Principal

1. Evento loaded envia árvore e host-port; mensagens abrem/escrevem/criam paths; watcher envia mudanças com debounce 1s; proxy conecta Docker socket. 🟢
2. Atualizar estado e devolver resultado ao consumidor. 🟢

## Fluxos Alternativos

- **Falha:** Erros são apenas logados; path de cliente não é confinado ao workspace. 🟢 🟢
- **Divergência do legado:** upgrade não autentica nem valida owner/path em cada comando. 🔴 Contrato alvo confirmado exige sessão Django, autorização por projeto e path confinado. 🟢

## Dependências

- ws, Dockerode, fs/promises, chokidar, directory-tree 🟢

## Decisões de Design Identificadas

| Decisão | Evidência no código | Confiança |
|---|---|---|
| Preservar integração existente e serialização de estado. | `projects-api/api/websocket/api_websocket.js:6` | 🟢 |
| Aplicar limites e fluxo de recursos declarados. | `projects-api/api/websocket/docker_websocket.js:3` | 🟢 |

## Estado Interno

Conteúdo de arquivos fica no diretório de workspace bind-mounted; referências a ComputerUnit e sockets são mantidas em `Map` somente durante a vida do processo. 🟢

## Observabilidade

Erros são logados nas fontes citadas; métricas distribuídas não foram encontradas. 🟢

## Riscos e Lacunas

- O legado não autentica upgrades nem valida owner/caminho em todos os comandos. 🔴 O contrato alvo confirmado exige autenticação Django, autorização por projeto em cada operação e caminho confinado ao workspace. 🟢

