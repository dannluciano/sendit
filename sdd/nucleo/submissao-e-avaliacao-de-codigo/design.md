# Submissão e avaliação de código, Design Técnico

## Interface

| Símbolo | Assinatura | Retorno | Observação |
|---|---|---|---|
| `create_submission` | conforme origem | entidade/resposta do fluxo | 🟢 |
| `run_submission_runner` | conforme origem | entidade/resposta do fluxo | 🟢 |
| `run_process` | conforme origem | entidade/resposta do fluxo | 🟢 |
| `compare_outputs` | conforme origem | entidade/resposta do fluxo | 🟢 |

## Fluxo Principal

1. View bloqueia duplicidade/intervalo, persiste Waiting e enfileira UUID; worker executa casos e salva primeiro erro ou sucesso. 🟢
2. Persistir estado e resultado nas entidades do módulo. 🟢

## Fluxos Alternativos

- **Falha:** Compilação/runtime/timeout/diff geram status específico. 🟢
- **Sem casos:** estado alvo deve ser `OK`, conforme decisão do usuário; o legado mantém `Waiting`. 🟢
- **Lacuna:** Política de retry da fila requer validação da configuração operacional. 🔴

## Dependências

- Redis/django-rq 🟢
- Docker Engine/imagens 🟢
- Question, CaseTest, Submission 🟢

## Decisões de Design Identificadas

| Decisão | Evidência no código | Confiança |
|---|---|---|
| Manter contrato de domínio e persistência atuais. | `core/views.py:213` | 🟢 |
| Preservar integração de processamento/cache configurada no legado. | `core/worker.py:5` | 🟢 |

## Estado Interno

Estado durável fica nos modelos do módulo; fila/cache transitórios seguem as dependências citadas. 🟢

## Observabilidade

Usar logs e campos de resultado existentes nos arquivos citados; não foi inferida telemetria adicional. 🟢

## Riscos e Lacunas

- Política de retry da fila requer validação da configuração operacional. 🔴
- Consulta de status alvo restrita ao autor/staff; o legado diverge em `core/views.py:310`. 🟢 Confirmado pelo usuário.

