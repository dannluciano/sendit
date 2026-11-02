# API de projetos, Requirements

## Visão Geral

Serviço Node/Hono provisiona workspaces Docker e integra IDE pelo navegador via HTTP/WebSocket. 🟢

## Responsabilidades

- Boot conecta Docker e prepara imagem; /api verifica cookie assinado; create provisiona ComputerUnit e mapas locais registram estado. 🟢
- Estado é guardado em Maps de processo; /version não está no prefixo /api protegido. 🟢

## Regras de Negócio

- Estado é guardado em Maps de processo; /version não está no prefixo /api protegido. 🟢
- Falha Docker encerra processo; erro de criação retorna 500; upgrade websocket não usa middleware HTTP. 🟢
- O contrato alvo requer sessão Django e owner do projeto validados em cada WebSocket; política confirmada pelo usuário. 🟢 O legado atual não comprova esse vínculo. 🔴

## Requisitos Funcionais

| ID | Requisito | Prioridade | Critério de Aceite |
|---|---|---|---|
| RF-01 | Implementar fluxo principal desta unit. 🟢 | Must | Boot conecta Docker e prepara imagem; /api verifica cookie assinado; create provisiona ComputerUnit e mapas locais registram estado. |
| RF-02 | Persistir/consultar estado e integração descrita. 🟢 | Must | Resultado corresponde aos campos e relações documentados. |
| RF-03 | Tratar falha e validar autorização. 🟡 | Must | Falha Docker encerra processo; erro de criação retorna 500; upgrade websocket não usa middleware HTTP. 🟢 |

## Requisitos Não Funcionais

| Tipo | Requisito inferido | Evidência no código | Confiança |
|---|---|---|---|
| Segurança | Validar sessão, owner e caminho antes de acesso. | `projects-api/api/app.js:1` | 🟢 |
| Performance | Preservar limites, SQL/debounce/integração já declarados. | `projects-api/api/routes.js:9` | 🟢 |

## Critérios de Aceitação

```gherkin
# 🟢 Happy path
Dado usuário e dados válidos
Quando executa o fluxo principal
Então Boot conecta Docker e prepara imagem; /api verifica cookie assinado; create provisiona ComputerUnit e mapas locais registram estado.

# 🟢 Falha
Dado recurso ausente ou usuário sem autorização
Quando solicita a operação
Então Falha Docker encerra processo; erro de criação retorna 500; upgrade websocket não usa middleware HTTP. 🟢
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
| `projects-api/api/app.js` | implementação descrita | 🟢 |
| `projects-api/api/routes.js` | implementação descrita | 🟢 |
| `projects-api/api/auth/auth_middleware.js` | implementação descrita | 🟢 |

