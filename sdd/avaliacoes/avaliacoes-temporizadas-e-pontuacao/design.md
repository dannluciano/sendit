# Avaliações temporizadas e pontuação, Design Técnico

## Interface

| Símbolo | Assinatura | Retorno | Observação |
|---|---|---|---|
| `Assessment.is_available` | conforme implementação | entidade/resposta | 🟢 |
| `AssessmentSubmission.compute_score` | conforme implementação | entidade/resposta | 🟢 |
| `validate_submission_datetime` | conforme implementação | entidade/resposta | 🟢 |
| `assessment_start` | conforme implementação | entidade/resposta | 🟢 |

## Fluxo Principal

1. A participação é criada/recuperada por avaliação e aluno; compute_score filtra submissões OK no intervalo, soma pontos por questão e salva score. 🟢
2. Persistir estado/resultado nos modelos relacionados. 🟢

## Fluxos Alternativos

- **Recurso inválido ou falha:** Submissões fora dos limites estritos não contam; clean contém validação de datas, mas não é chamada automaticamente pelo save observado. 🟢
- **Lacuna:** Não há constraint visível de participação única por avaliação/aluno; concorrência pode criar duplicatas. 🔴

## Dependências

- core.Question/Submission 🟢
- QuestionInfo 🟢
- timezone-aware datetime Django 🟢

## Decisões de Design Identificadas

| Decisão | Evidência no código | Confiança |
|---|---|---|
| Persistir entidades pelo ORM e separar processamento em função/worker quando aplicável. | `evaluation/models.py:39` | 🟢 |
| Manter integração com os módulos compartilhados. | `evaluation/models.py:96` | 🟢 |

## Estado Interno

Estado durável fica nos modelos da unit; trabalhos assíncronos e resultados transitórios seguem fluxo RQ quando aplicável. 🟢

## Observabilidade

Registros e resultados de execução são os sinais observados; métricas adicionais não foram identificadas. 🟢

## Riscos e Lacunas

- Não há constraint visível de participação única por avaliação/aluno; concorrência pode criar duplicatas. 🔴
- A autorização por proprietário não existe nos endpoints atuais por UUID. 🔴 O contrato alvo confirmado exige janela ativa e filtro por aluno/staff. 🟢

## Contrato Alvo Confirmado pelo Usuário

Antes de criar ou exibir participação, a view valida a janela ativa (limites estritos conforme `Assessment.is_available`). A consulta filtra pelo aluno autenticado ou permite staff autorizado. 🟢 Confirmado em 2026-11-02; o legado atual não aplica essas verificações em todas as rotas.

