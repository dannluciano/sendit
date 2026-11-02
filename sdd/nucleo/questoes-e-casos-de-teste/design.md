# Questões e casos de teste, Design Técnico

## Interface

| Símbolo | Assinatura | Retorno | Observação |
|---|---|---|---|
| `Question` | conforme função/classe de origem | entidade ou resposta da unit | Contrato confirmado no legado. 🟢 |
| `CaseTest` | conforme função/classe de origem | entidade ou resposta da unit | Contrato confirmado no legado. 🟢 |
| `home` | conforme função/classe de origem | entidade ou resposta da unit | Contrato confirmado no legado. 🟢 |
| `QuestionAdmin` | conforme função/classe de origem | entidade ou resposta da unit | Contrato confirmado no legado. 🟢 |

## Fluxo Principal

1. A view carrega questões ainda não resolvidas, restringe a visíveis, aplica busca/tags e ordena/limita resultados; o detalhe é recuperado por ID ou UUID. 🟢
2. Persistir estado e resultado usando os modelos/serviços listados em `requirements.md`. 🟢

## Fluxos Alternativos

- **Erro/ausência:** Questão invisível no detalhe por ID retorna não encontrado; busca inválida não deve aplicar filtro parcial. 🟢
- **Lacuna:** Não foi identificada regra que exija ao menos um caso de teste por questão. 🔴

## Dependências

- Django ORM e PostgreSQL 🟢
- Django Admin 🟢
- auth.User e Submission 🟢

## Decisões de Design Identificadas

| Decisão | Evidência no código | Confiança |
|---|---|---|
| Manter o contrato atual de domínio e separar persistência do fluxo de apresentação. | `core/models.py:87` | 🟢 |
| Preservar o comportamento assíncrono/consulta do legado quando aplicável. | `core/views.py:63` | 🟢 |

## Estado Interno

O estado durável fica nas entidades e campos descritos nos modelos do legado; estado transitório, se aplicável, é mantido pelo worker/cache identificado acima. 🟢

## Observabilidade

A unit usa os logs/retornos observados nos arquivos citados; não foi inferida telemetria adicional. 🟢

## Riscos e Lacunas

- Não foi identificada regra que exija ao menos um caso de teste por questão. 🔴
- Páginas da unit exigem autenticação; detalhes de retenção das questões não foram definidos nesta análise. 🟡

