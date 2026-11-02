# Provisionamento do workspace, Design Técnico

## Interface

| Símbolo | Assinatura | Retorno | Observação |
|---|---|---|---|
| `projects-api/api/computer_unit/computer_unit_controller.js:13` | API/worker/model conforme fonte | entidade, resposta ou evento | 🟢 |
| `projects-api/api/computer_unit/computer_unit_service.js:12` | API/worker/model conforme fonte | entidade, resposta ou evento | 🟢 |
| `projects-api/api/computer_unit/temp_dir.js:11` | API/worker/model conforme fonte | entidade, resposta ou evento | 🟢 |

## Fluxo Principal

1. Controller lê project/settings; service cria temp dir, mapeia envs, monta volume, cria/inicia container e retorna ComputerUnit. 🟢
2. Atualizar estado e devolver resultado ao consumidor. 🟢

## Fluxos Alternativos

- **Falha:** Erro do serviço vira mensagem genérica; restart perde Maps de estado. 🟢 🟢
- **Lacuna:** Limpeza de diretórios temporários e restauração de ambientes após restart não estão cobertas. 🔴

## Dependências

- Dockerode, filesystem host/guest compartilhado, configs e payload Project 🟢

## Decisões de Design Identificadas

| Decisão | Evidência no código | Confiança |
|---|---|---|
| Preservar integração existente e serialização de estado. | `projects-api/api/computer_unit/computer_unit_controller.js:13` | 🟢 |
| Aplicar limites e fluxo de recursos declarados. | `projects-api/api/computer_unit/computer_unit_service.js:12` | 🟢 |

## Estado Interno

As associações de ComputerUnit são transitórias em `Map`; arquivos do workspace ficam no diretório host compartilhado com o container. O mapeamento não é recuperado após restart do serviço. 🟢

## Observabilidade

Erros são logados nas fontes citadas; métricas distribuídas não foram encontradas. 🟢

## Riscos e Lacunas

- Restauração de ambiente após restart não está coberta. 🔴 Cleanup de container/workspace ao excluir projeto é requisito confirmado, mas não implementado no legado. 🟢

