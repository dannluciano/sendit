# Ranking e conquistas, Design Técnico

## Interface

| Símbolo | Assinatura | Retorno | Observação |
|---|---|---|---|
| `get_best_users_of_week` | conforme origem | entidade/resposta do fluxo | 🟢 |
| `compute_bests_of_week` | conforme origem | entidade/resposta do fluxo | 🟢 |
| `get_leaderboard` | conforme origem | entidade/resposta do fluxo | 🟢 |
| `compute_leaderboard` | conforme origem | entidade/resposta do fluxo | 🟢 |

## Fluxo Principal

1. Consultas agregam submissões OK e conquistas; ranking filtra por grupo, usa cache e apresenta 50 por página. 🟢
2. Persistir estado e resultado nas entidades do módulo. 🟢

## Fluxos Alternativos

- **Falha:** Falha na rotina semanal é capturada/logada; usuário inexistente não tem fallback no lookup. 🟢
- **Lacuna:** TTL e invalidação de cache não são definidos no fluxo observado. 🔴

## Dependências

- Submission/Question/Achievement/User 🟢
- PostgreSQL 🟢
- Redis cache 🟢

## Decisões de Design Identificadas

| Decisão | Evidência no código | Confiança |
|---|---|---|
| Manter contrato de domínio e persistência atuais. | `core/domain.py:45` | 🟢 |
| Preservar integração de processamento/cache configurada no legado. | `core/domain.py:136` | 🟢 |

## Estado Interno

Estado durável fica nos modelos do módulo; fila/cache transitórios seguem as dependências citadas. 🟢

## Observabilidade

Usar logs e campos de resultado existentes nos arquivos citados; não foi inferida telemetria adicional. 🟢

## Riscos e Lacunas

- TTL e invalidação de cache não são definidos no fluxo observado. 🔴
- TTL/invalidação do cache de ranking não estão definidos no fluxo observado. 🔴

