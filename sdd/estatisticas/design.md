# Estatísticas, Design Técnico

## Interface

| Símbolo | Assinatura | Retorno | Observação |
|---|---|---|---|
| `statistics/models.py:13` | API/worker/model conforme fonte | entidade, resposta ou evento | 🟢 |
| `statistics/domain.py:9` | API/worker/model conforme fonte | entidade, resposta ou evento | 🟢 |
| `statistics/middleware.py:10` | API/worker/model conforme fonte | entidade, resposta ou evento | 🟢 |
| `statistics/models.py:67` | API/worker/model conforme fonte | entidade, resposta ou evento | 🟢 |

## Fluxo Principal

1. Signals criam/fecham LogRecord; middleware atualiza registro mais recente em respostas 200 autenticadas não estáticas; SQL views agregam submissões. 🟢
2. Atualizar estado e devolver resultado ao consumidor. 🟢

## Fluxos Alternativos

- **Falha:** Sem LogRecord anterior, atualização não cria; X-Forwarded-For é usado integralmente. 🟢 🟢
- **Lacuna:** Sessões simultâneas e confiança no proxy para X-Forwarded-For não estão definidas. 🔴

## Dependências

- Django auth signals/middleware, core Submission/Question, PostgreSQL 🟢

## Decisões de Design Identificadas

| Decisão | Evidência no código | Confiança |
|---|---|---|
| Preservar integração existente e serialização de estado. | `statistics/models.py:13` | 🟢 |
| Aplicar limites e fluxo de recursos declarados. | `statistics/domain.py:9` | 🟢 |

## Estado Interno

Estado durável fica no banco; estado transitório fica em processo/container conforme código citado. 🟢

## Observabilidade

Erros são logados nas fontes citadas; métricas distribuídas não foram encontradas. 🟢

## Riscos e Lacunas

- Sessões simultâneas e confiança no proxy para X-Forwarded-For não estão definidas. 🔴

