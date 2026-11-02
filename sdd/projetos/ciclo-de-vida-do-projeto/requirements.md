# Ciclo de vida do projeto, Requirements

## Visão Geral

Valida nome, cria/reutiliza projeto por usuário, serializa dados e exclui projeto próprio. 🟢

## Responsabilidades

- Form válido chama get_or_create(name, owner); detalhe filtra nome+owner e inclui temp_dir/UUID; exclusão exige POST. 🟢
- Nome até 100 chars, alfanumérico ASCII, hífen/underscore e único por owner. 🟢

## Regras de Negócio

- Nome até 100 chars, alfanumérico ASCII, hífen/underscore e único por owner. 🟢
- Form inválido reaparece; recurso ausente/alheio retorna 404. 🟢
- Excluir projeto deve parar/remover seu container e apagar o workspace. 🟢 Confirmado pelo usuário em 2026-11-02; o legado atual remove apenas o registro `Project`.

## Requisitos Funcionais

| ID | Requisito | Prioridade | Critério de Aceite |
|---|---|---|---|
| RF-01 | Implementar fluxo principal desta unit. 🟢 | Must | Form válido chama get_or_create(name, owner); detalhe filtra nome+owner e inclui temp_dir/UUID; exclusão exige POST. |
| RF-02 | Persistir/consultar estado e integração descrita. 🟢 | Must | Resultado corresponde aos campos e relações documentados. |
| RF-03 | Tratar falha e validar autorização. 🟡 | Must | Form inválido reaparece; recurso ausente/alheio retorna 404. 🟢 |

## Requisitos Não Funcionais

| Tipo | Requisito inferido | Evidência no código | Confiança |
|---|---|---|---|
| Segurança | Validar sessão, owner e caminho antes de acesso. | `projects/forms.py:6` | 🟢 |
| Performance | Preservar limites, SQL/debounce/integração já declarados. | `projects/views.py:46` | 🟢 |

## Critérios de Aceitação

```gherkin
# 🟢 Happy path
Dado usuário e dados válidos
Quando executa o fluxo principal
Então Form válido chama get_or_create(name, owner); detalhe filtra nome+owner e inclui temp_dir/UUID; exclusão exige POST.

# 🟢 Falha
Dado recurso ausente ou usuário sem autorização
Quando solicita a operação
Então Form inválido reaparece; recurso ausente/alheio retorna 404. 🟢
```

## Prioridade (MoSCoW)

| Requisito | MoSCoW | Justificativa |
|---|---|---|
| Fluxo principal | Must | Caminho central do domínio. 🟢 |
| Persistência/integração | Must | Necessária para resultado completo. 🟢 |
| Limites e autorização | Must | Integridade e segurança operacional. 🟡 |

## Rastreabilidade de Código

| Arquivo | Função / Classe | Cobertura |
|---|---|---|
| `projects/forms.py` | implementação descrita | 🟢 |
| `projects/views.py` | implementação descrita | 🟢 |
| `projects/models.py` | implementação descrita | 🟢 |
| `projects/views.py` | implementação descrita | 🟢 |

