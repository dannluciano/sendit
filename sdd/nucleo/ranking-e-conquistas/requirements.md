# Ranking e conquistas, Requirements

## Visão Geral

Calcula XP e nível, exibe classificação/perfil e concede reconhecimento semanal. 🟢

## Responsabilidades

- Exibir ranking geral/por grupo. 🟢
- Agregar XP, nível e conquistas. 🟢
- Conceder conquista semanal. 🟢

## Regras de Negócio

- XP agrega questões OK e conquistas; nível sqrt(XP questão)*1.5, teto 74. 🟢
- Grupo Staff excluído; filtro all não filtra grupo. 🟢
- Top três da semana anterior recebem conquista oculta semanal. 🟢
- TTL e invalidação de cache não são definidos no fluxo observado. 🔴

## Requisitos Funcionais

| ID | Requisito | Prioridade | Critério de Aceite |
|---|---|---|---|
| RF-01 | Exibir ranking geral/por grupo. 🟢 | Must | Filtro e campos de posição/XP/nível/grupo funcionam. |
| RF-02 | Agregar XP, nível e conquistas. 🟢 | Must | Perfil reflete fontes documentadas. |
| RF-03 | Conceder conquista semanal. 🟢 | Should | Badge da semana associado aos três elegíveis. |

## Requisitos Não Funcionais

| Tipo | Requisito inferido | Evidência no código | Confiança |
|---|---|---|---|
| Segurança | Preservar autenticação e propriedade do recurso quando observadas. | `core/domain.py:45` | 🟢 |
| Performance | Preservar o uso de fila/cache/limites existente. | `core/domain.py:136` | 🟢 |

## Critérios de Aceitação

```gherkin
# 🟢 Happy path
Dado ranking e conquistas válidos e usuário autorizado
Quando executa o fluxo principal
Então Consultas agregam submissões OK e conquistas; ranking filtra por grupo, usa cache e apresenta 50 por página.

# 🟢 Falha
Dado condição inválida ou recurso ausente
Quando o usuário executa a ação
Então Falha na rotina semanal é capturada/logada; usuário inexistente não tem fallback no lookup.
```

## Prioridade (MoSCoW)

| Requisito | MoSCoW | Justificativa |
|---|---|---|
| Exibir ranking geral/por grupo. 🟢 | Must | Fluxo central da unit. 🟢 |
| Agregar XP, nível e conquistas. 🟢 | Must | Regra de domínio essencial. 🟢 |
| Conceder conquista semanal. 🟢 | Should | Capacidade complementar importante. 🟡 |

## Rastreabilidade de Código

| Arquivo | Função / Classe | Cobertura |
|---|---|---|
| `core/domain.py` | implementação descrita | 🟢 |
| `core/domain.py` | implementação descrita | 🟢 |
| `core/domain.py` | implementação descrita | 🟢 |

