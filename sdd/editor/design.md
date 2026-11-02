# Editor, Design Técnico

## Interface

| Símbolo | Assinatura | Retorno | Observação |
|---|---|---|---|
| `Runner` | conforme implementação | entidade/resposta | 🟢 |
| `FileCode` | conforme implementação | entidade/resposta | 🟢 |
| `create_runner` | conforme implementação | entidade/resposta | 🟢 |
| `run_submission_from_editor` | conforme implementação | entidade/resposta | 🟢 |

## Fluxo Principal

1. Usuário autenticado executa código pela fila RQ e salva/lista/abre/baixa/exclui seus arquivos. 🟢
2. Persistir estado/resultado nos modelos relacionados. 🟢

## Fluxos Alternativos

- **Recurso inválido ou falha:** Runner ou arquivo consultado por UUID sem correspondência resulta em 404 onde explicitamente tratado; ownership não é validado em várias views. 🟢
- **Divergência do legado:** views por UUID não conferem autoria. 🔴 Contrato alvo confirmado exige owner/staff para arquivos e Runners. 🟢

## Dependências

- core.SubmissionRunnerManager 🟢
- Redis/django-rq 🟢
- auth.User 🟢

## Decisões de Design Identificadas

| Decisão | Evidência no código | Confiança |
|---|---|---|
| Persistir entidades pelo ORM e separar processamento em função/worker quando aplicável. | `editor/models.py:10` | 🟢 |
| Manter integração com os módulos compartilhados. | `editor/views.py:28` | 🟢 |

## Estado Interno

Estado durável fica nos modelos da unit; trabalhos assíncronos e resultados transitórios seguem fluxo RQ quando aplicável. 🟢

## Observabilidade

Registros e resultados de execução são os sinais observados; métricas adicionais não foram identificadas. 🟢

## Riscos e Lacunas

- Legado não filtra owner em views por UUID; contrato alvo confirmado exige owner/staff. 🟢
- Contrato alvo validado: operações de arquivos e Runner são restritas ao owner/staff autorizado. 🟢 Confirmado pelo usuário; legado diverge.

