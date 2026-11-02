# Submissão e avaliação de código, Requirements

## Visão Geral

Recebe código e avalia programas em workers assíncronos usando casos de teste. 🟢

## Responsabilidades

- Criar e enfileirar submissão por UUID. 🟢
- Executar casos até falha ou sucesso. 🟢
- Classificar/persistir saída, status e log. 🟢

## Regras de Negócio

- Usuário autenticado envia submissão. 🟢
- Questão resolvida bloqueia novos envios; intervalo mínimo é 15 segundos. 🟢
- Worker para no primeiro caso não OK. 🟢
- Docker usa limites e timeout de 4s, 6s Java, sem rede. 🟢
- O produto deve aprovar (`OK`) submissões de questões sem casos de teste, conforme confirmação do usuário; o legado atual deixa o status `Waiting`. 🟢

## Requisitos Funcionais

| ID | Requisito | Prioridade | Critério de Aceite |
|---|---|---|---|
| RF-01 | Criar e enfileirar submissão por UUID. 🟢 | Must | Registro Waiting e job com UUID. |
| RF-02 | Executar casos até falha ou sucesso. 🟢 | Must | Primeira falha interrompe o worker. |
| RF-03 | Classificar/persistir saída, status e log. 🟢 | Must | Erros conhecidos ficam distinguíveis. |

## Requisitos Não Funcionais

| Tipo | Requisito inferido | Evidência no código | Confiança |
|---|---|---|---|
| Segurança | Preservar autenticação e propriedade do recurso quando observadas. | `core/views.py:213` | 🟢 |
| Performance | Preservar o uso de fila/cache/limites existente. | `core/worker.py:5` | 🟢 |

## Critérios de Aceitação

```gherkin
# 🟢 Happy path
Dado submissão e avaliação de código válidos e usuário autorizado
Quando executa o fluxo principal
Então View bloqueia duplicidade/intervalo, persiste Waiting e enfileira UUID; worker executa casos e salva primeiro erro ou sucesso.

# 🟢 Falha
Dado condição inválida ou recurso ausente
Quando o usuário executa a ação
Então compilação/runtime/timeout/diff geram status específico; sem casos a submissão é aprovada conforme decisão do usuário, embora o legado atual deixe Waiting.
```

## Prioridade (MoSCoW)

| Requisito | MoSCoW | Justificativa |
|---|---|---|
| Criar e enfileirar submissão por UUID. 🟢 | Must | Fluxo central da unit. 🟢 |
| Executar casos até falha ou sucesso. 🟢 | Must | Regra de domínio essencial. 🟢 |
| Classificar/persistir saída, status e log. 🟢 | Should | Capacidade complementar importante. 🟡 |

## Rastreabilidade de Código

| Arquivo | Função / Classe | Cobertura |
|---|---|---|
| `core/views.py` | implementação descrita | 🟢 |
| `core/worker.py` | implementação descrita | 🟢 |
| `core/submission_runner.py` | implementação descrita | 🟢 |

## Decisões Confirmadas pelo Usuário

- Questão sem casos de teste deve resultar em submissão aprovada (`OK`). 🟢 Confirmado em 2026-11-02; o legado atual mantém `Waiting` em `core/worker.py:5`.
- Consulta de status deve ser restrita ao autor e a staff autorizado. 🟢 Confirmado em 2026-11-02; a view atual não aplica essa checagem em `core/views.py:310`.

