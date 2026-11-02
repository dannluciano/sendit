# Arquivos de código, Requirements

## Visão Geral

Salva, lista, abre, baixa e exclui arquivos associados a uma conta. 🟢

## Responsabilidades

- FileCode associa owner, nome, código, linguagem e datas. 🟢
- save usa update_or_create por nome+owner; list filtra owner; detalhe/download/exclusão usam UUID. 🟢

## Regras de Negócio

- FileCode associa owner, nome, código, linguagem e datas. 🟢
- UUID ausente dá 404; operações por UUID não filtram owner e linguagem de extensão desconhecida falha. 🟢
- Operações por UUID devem restringir acesso ao owner e a staff autorizado. 🟢 Confirmado pelo usuário; o legado atual não aplica esse filtro.

## Requisitos Funcionais

| ID | Requisito | Prioridade | Critério de Aceite |
|---|---|---|---|
| RF-01 | Implementar o fluxo principal da unit. 🟢 | Must | save usa update_or_create por nome+owner; list filtra owner; detalhe/download/exclusão usam UUID. |
| RF-02 | Persistir e recuperar entidades relacionadas. 🟢 | Must | Estado consultável após operação. |
| RF-03 | Tratar falhas e restringir acesso ao owner/staff. 🟢 | Must | UUID alheio não é acessível; linguagem sem extensão mapeada retorna erro explícito. |

## Requisitos Não Funcionais

| Tipo | Requisito inferido | Evidência no código | Confiança |
|---|---|---|---|
| Segurança | Autenticação e propriedade do recurso devem ser verificadas. | `editor/models.py:39` | 🟢 |
| Performance | Preservar consultas e formato de persistência existentes. | `editor/views.py:60` | 🟢 |

## Critérios de Aceitação

```gherkin
# 🟢 Happy path
Dado usuário autenticado e recurso válido
Quando executa o fluxo principal
Então save usa update_or_create por nome+owner; list filtra owner; detalhe/download/exclusão usam UUID.

# 🟢 Falha
Dado recurso ausente ou usuário sem autorização
Quando solicita a operação
Então UUID ausente dá 404; acesso a owner alheio é negado e linguagem de extensão desconhecida falha explicitamente.
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
| `editor/models.py` | regra desta unit | 🟢 |
| `editor/views.py` | regra desta unit | 🟢 |
| `editor/views.py` | regra desta unit | 🟢 |
| `editor/views.py` | regra desta unit | 🟢 |

