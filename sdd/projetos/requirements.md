# Projetos, Requirements

## Visão Geral

Gerencia projetos pessoais e fornece dados para abrir o workspace da IDE. 🟢

## Responsabilidades

- Nome é único por owner e aceita letras ASCII, números, underscore e hífen. 🟢
- Usuário cria projeto validado, lista próprios projetos, consulta detalhe serializado e exclui via POST. 🟢

## Regras de Negócio

- Nome é único por owner e aceita letras ASCII, números, underscore e hífen. 🟢
- Form inválido é reexibido; projeto ausente/alheio não é encontrado. 🟢
- Ao excluir projeto, remover container e workspace. 🟢 Confirmado pelo usuário em 2026-11-02; o legado remove apenas o registro.

## Requisitos Funcionais

| ID | Requisito | Prioridade | Critério de Aceite |
|---|---|---|---|
| RF-01 | Implementar o fluxo principal da unit. 🟢 | Must | Usuário cria projeto validado, lista próprios projetos, consulta detalhe serializado e exclui via POST. |
| RF-02 | Persistir e recuperar entidades relacionadas. 🟢 | Must | Estado consultável após operação. |
| RF-03 | Tratar falhas e restringir acesso. 🟡 | Must | Form inválido é reexibido; projeto ausente/alheio não é encontrado. 🟢 |

## Requisitos Não Funcionais

| Tipo | Requisito inferido | Evidência no código | Confiança |
|---|---|---|---|
| Segurança | Autenticação e propriedade do recurso devem ser verificadas. | `projects/models.py:12` | 🟢 |
| Performance | Preservar consultas e formato de persistência existentes. | `projects/views.py:46` | 🟢 |

## Critérios de Aceitação

```gherkin
# 🟢 Happy path
Dado usuário autenticado e recurso válido
Quando executa o fluxo principal
Então Usuário cria projeto validado, lista próprios projetos, consulta detalhe serializado e exclui via POST.

# 🟢 Falha
Dado recurso ausente ou usuário sem autorização
Quando solicita a operação
Então Form inválido é reexibido; projeto ausente/alheio não é encontrado. 🟢
```

## Prioridade (MoSCoW)

| Requisito | MoSCoW | Justificativa |
|---|---|---|
| Fluxo principal | Must | Capacidade central da unit. 🟢 |
| Persistência e consulta | Must | Necessária para continuidade. 🟢 |
| Casos administrativos/erro | Should | Complementar à jornada principal. 🟡 |

## Rastreabilidade de Código

| Arquivo | Função / Classe | Cobertura |
|---|---|---|
| `projects/models.py` | regra desta unit | 🟢 |
| `projects/views.py` | regra desta unit | 🟢 |
| `projects/views.py` | regra desta unit | 🟢 |
| `projects/views.py` | regra desta unit | 🟢 |

