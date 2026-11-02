# Execução avulsa do editor, Design Técnico

## Interface

| Símbolo | Assinatura | Retorno | Observação |
|---|---|---|---|
| `create_runner` | conforme implementação | entidade/resposta | 🟢 |
| `runner_details` | conforme implementação | entidade/resposta | 🟢 |
| `run_submission_from_editor` | conforme implementação | entidade/resposta | 🟢 |

## Fluxo Principal

1. POST JSON cria Runner, agenda worker e responde UUID; worker executa linguagem via runner compartilhado e persiste status, saída e log. 🟢
2. Persistir estado/resultado nos modelos relacionados. 🟢

## Fluxos Alternativos

- **Recurso inválido ou falha:** Runner inexistente é logado e ignorado pelo worker; linguagem inválida/JSON inválido não tem tratamento explícito na view. 🟢
- **Contrato alvo:** consulta de Runner restrita ao owner e staff autorizado. 🟢 Confirmado pelo usuário; o legado atual não filtra owner.

## Dependências

- core.SubmissionRunnerManager 🟢
- django-rq/Redis 🟢
- Docker Engine 🟢

## Decisões de Design Identificadas

| Decisão | Evidência no código | Confiança |
|---|---|---|
| Persistir entidades pelo ORM e separar processamento em função/worker quando aplicável. | `editor/views.py:28` | 🟢 |
| Manter integração com os módulos compartilhados. | `editor/views.py:48` | 🟢 |

## Estado Interno

Estado durável fica nos modelos da unit; trabalhos assíncronos e resultados transitórios seguem fluxo RQ quando aplicável. 🟢

## Observabilidade

Registros e resultados de execução são os sinais observados; métricas adicionais não foram identificadas. 🟢

## Riscos e Lacunas

- A implementação alvo filtra consulta de Runner por owner/staff; o legado atual exige apenas login. 🟢 Confirmado pelo usuário em 2026-11-02.
- Contrato alvo validado: consulta de Runner restrita ao owner/staff autorizado. 🟢 Confirmado pelo usuário; legado diverge.

