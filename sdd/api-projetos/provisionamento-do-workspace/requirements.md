# Provisionamento do workspace, Requirements

## Visão Geral

Cria diretório compartilhado e container VM limitado para workspace de um projeto. 🟢

## Responsabilidades

- Controller lê project/settings; service cria temp dir, mapeia envs, monta volume, cria/inicia container e retorna ComputerUnit. 🟢
- 512 MiB, porta 8080, autoRemove e ulimits; storage quota 2GB em produção. 🟢

## Regras de Negócio

- 512 MiB, porta 8080, autoRemove e ulimits; storage quota 2GB em produção. 🟢
- Erro do serviço vira mensagem genérica; restart perde Maps de estado. 🟢
- Restauração de ambientes após restart não está coberta. 🔴 A exclusão de projeto deve remover container e workspace. 🟢 Confirmado pelo usuário em 2026-11-02.

## Requisitos Funcionais

| ID | Requisito | Prioridade | Critério de Aceite |
|---|---|---|---|
| RF-01 | Implementar fluxo principal desta unit. 🟢 | Must | Controller lê project/settings; service cria temp dir, mapeia envs, monta volume, cria/inicia container e retorna ComputerUnit. |
| RF-02 | Persistir/consultar estado e integração descrita. 🟢 | Must | Resultado corresponde aos campos e relações documentados. |
| RF-03 | Tratar falha e validar autorização. 🟡 | Must | Erro do serviço vira mensagem genérica; restart perde Maps de estado. 🟢 |

## Requisitos Não Funcionais

| Tipo | Requisito inferido | Evidência no código | Confiança |
|---|---|---|---|
| Segurança | Validar sessão, owner e caminho antes de acesso. | `projects-api/api/computer_unit/computer_unit_controller.js:13` | 🟢 |
| Performance | Preservar limites, SQL/debounce/integração já declarados. | `projects-api/api/computer_unit/computer_unit_service.js:12` | 🟢 |

## Critérios de Aceitação

```gherkin
# 🟢 Happy path
Dado usuário e dados válidos
Quando executa o fluxo principal
Então Controller lê project/settings; service cria temp dir, mapeia envs, monta volume, cria/inicia container e retorna ComputerUnit.

# 🟢 Falha
Dado recurso ausente ou usuário sem autorização
Quando solicita a operação
Então Erro do serviço vira mensagem genérica; restart perde Maps de estado. 🟢
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
| `projects-api/api/computer_unit/computer_unit_controller.js` | implementação descrita | 🟢 |
| `projects-api/api/computer_unit/computer_unit_service.js` | implementação descrita | 🟢 |
| `projects-api/api/computer_unit/temp_dir.js` | implementação descrita | 🟢 |

