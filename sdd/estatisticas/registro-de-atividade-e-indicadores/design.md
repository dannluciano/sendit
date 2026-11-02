# Registro de atividade e indicadores, Design Técnico

## Interface

| Símbolo | Assinatura | Retorno | Observação |
|---|---|---|---|
| `statistics/models.py:13` | API/worker/model conforme fonte | entidade, resposta ou evento | 🟢 |
| `statistics/domain.py:22` | API/worker/model conforme fonte | entidade, resposta ou evento | 🟢 |
| `statistics/models.py:67` | API/worker/model conforme fonte | entidade, resposta ou evento | 🟢 |
| `statistics/models.py:122` | API/worker/model conforme fonte | entidade, resposta ou evento | 🟢 |

## Fluxo Principal

1. Login cria LogRecord; navegação atualiza check_out/IP; views SQL calculam XP, nível, taxas e contagens. 🟢
2. Atualizar estado e devolver resultado ao consumidor. 🟢

## Fluxos Alternativos

- **Falha:** Sem registro aberto, set_last_activity não insere; SQL depende de sintaxe PostgreSQL. 🟢 🟢
- **Lacuna:** IP forwarded e concorrência de múltiplas sessões precisam definição. 🔴

## Dependências

- Django signals, middleware, PostgreSQL e tabelas core 🟢

## Decisões de Design Identificadas

| Decisão | Evidência no código | Confiança |
|---|---|---|
| Preservar integração existente e serialização de estado. | `statistics/models.py:13` | 🟢 |
| Aplicar limites e fluxo de recursos declarados. | `statistics/domain.py:22` | 🟢 |

## Estado Interno

Estado durável fica no banco; estado transitório fica em processo/container conforme código citado. 🟢

## Observabilidade

Erros são logados nas fontes citadas; métricas distribuídas não foram encontradas. 🟢

## Riscos e Lacunas

- IP forwarded e concorrência de múltiplas sessões precisam definição. 🔴

