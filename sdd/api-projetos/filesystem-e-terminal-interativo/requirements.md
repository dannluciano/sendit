# Filesystem e terminal interativo, Requirements

## Visão Geral

Sincroniza árvore de arquivos, lê/escreve no workspace e encaminha terminal via WebSocket para Docker. 🟢

## Responsabilidades

- Evento loaded envia árvore e host-port; mensagens abrem/escrevem/criam paths; watcher envia mudanças com debounce 1s; proxy conecta Docker socket. 🟢
- write/writeInPath verificam parcialmente ownerUUID; mkdir/open não verificam owner; close para container. 🟢

## Regras de Negócio

- write/writeInPath verificam parcialmente ownerUUID; mkdir/open não verificam owner; close para container. 🟢
- Erros são apenas logados; path de cliente não é confinado ao workspace. 🟢
- Contrato alvo confirmado: autenticar sessão Django, verificar proprietário em cada operação e confinar caminhos ao workspace. 🟢 Confirmado pelo usuário em 2026-11-02; o legado atual não cumpre integralmente esta política.

## Requisitos Funcionais

| ID | Requisito | Prioridade | Critério de Aceite |
|---|---|---|---|
| RF-01 | Implementar fluxo principal desta unit. 🟢 | Must | Evento loaded envia árvore e host-port; mensagens abrem/escrevem/criam paths; watcher envia mudanças com debounce 1s; proxy conecta Docker socket. |
| RF-02 | Persistir/consultar estado e integração descrita. 🟢 | Must | Resultado corresponde aos campos e relações documentados. |
| RF-03 | Tratar falha e validar autorização/confinamento de caminho. 🟢 | Must | Mensagens não autorizadas e caminhos fora do workspace são rejeitados. |

## Requisitos Não Funcionais

| Tipo | Requisito inferido | Evidência no código | Confiança |
|---|---|---|---|
| Segurança | Validar sessão, owner e caminho antes de acesso. | `projects-api/api/websocket/api_websocket.js:6` | 🟢 |
| Performance | Preservar limites, SQL/debounce/integração já declarados. | `projects-api/api/websocket/docker_websocket.js:3` | 🟢 |

## Critérios de Aceitação

```gherkin
# 🟢 Happy path
Dado usuário e dados válidos
Quando executa o fluxo principal
Então Evento loaded envia árvore e host-port; mensagens abrem/escrevem/criam paths; watcher envia mudanças com debounce 1s; proxy conecta Docker socket.

# 🟢 Falha
Dado recurso ausente ou usuário sem autorização
Quando solicita a operação
Então sessão/owner inválidos e caminhos fora do workspace são rejeitados antes de acessar arquivos.
```

## Prioridade (MoSCoW)

| Requisito | MoSCoW | Justificativa |
|---|---|---|
| Fluxo principal | Must | Caminho central do domínio. 🟢 |
| Persistência/integração | Must | Necessária para resultado completo. 🟢 |
| Limites e autorização | Must | Integridade e segurança operacional. 🟡 |

## Rastreabilidade de Código

| Arquivo | Função / Classe | Cobertura |
|---|---|---|
| `projects-api/api/websocket/api_websocket.js` | implementação descrita | 🟢 |
| `projects-api/api/websocket/docker_websocket.js` | implementação descrita | 🟢 |
| `projects-api/api/computer_unit/temp_dir.js` | implementação descrita | 🟢 |

