# Avaliações, Design Técnico

## Interface

| Símbolo | Assinatura | Retorno | Observação |
|---|---|---|---|
| `Assessment` | conforme implementação | entidade/resposta | 🟢 |
| `QuestionInfo` | conforme implementação | entidade/resposta | 🟢 |
| `AssessmentSubmission` | conforme implementação | entidade/resposta | 🟢 |
| `assessment_detail` | conforme implementação | entidade/resposta | 🟢 |

## Fluxo Principal

1. Usuário autenticado consulta avaliações dos seus grupos dentro do período; inicia participação e acompanha questões corretas e pontuação. 🟢
2. Persistir estado/resultado nos modelos relacionados. 🟢

## Fluxos Alternativos

- **Recurso inválido ou falha:** UUID inválido retorna não encontrado; dados por UUID não são filtrados pelo autor no detalhe atual. 🟢
- **Divergência do legado:** `assessment_start` não chama `is_available()` e detalhe por UUID não verifica autoria. 🔴 Contrato alvo confirmado exige janela ativa e autorização por autor/staff. 🟢

## Dependências

- core.Question e core.Submission 🟢
- auth.User e auth.Group 🟢
- Django ORM/PostgreSQL 🟢

## Decisões de Design Identificadas

| Decisão | Evidência no código | Confiança |
|---|---|---|
| Persistir entidades pelo ORM e separar processamento em função/worker quando aplicável. | `evaluation/models.py:13` | 🟢 |
| Manter integração com os módulos compartilhados. | `evaluation/views.py:10` | 🟢 |

## Estado Interno

Estado durável fica nos modelos da unit; trabalhos assíncronos e resultados transitórios seguem fluxo RQ quando aplicável. 🟢

## Observabilidade

Registros e resultados de execução são os sinais observados; métricas adicionais não foram identificadas. 🟢

## Riscos e Lacunas

- No legado, `assessment_start` não chama `is_available()` e detalhe por UUID não verifica autoria. 🔴 A política alvo está confirmada e descrita acima. 🟢
- Contrato alvo validado: verificar janela da avaliação e filtrar participação pelo aluno ou staff autorizado. 🟢 Confirmado pelo usuário; legado diverge.

