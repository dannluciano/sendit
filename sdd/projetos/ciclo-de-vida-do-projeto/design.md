# Ciclo de vida do projeto, Design Técnico

## Interface

| Símbolo | Assinatura | Retorno | Observação |
|---|---|---|---|
| `projects/forms.py:6` | API/worker/model conforme fonte | entidade, resposta ou evento | 🟢 |
| `projects/views.py:46` | API/worker/model conforme fonte | entidade, resposta ou evento | 🟢 |
| `projects/models.py:54` | API/worker/model conforme fonte | entidade, resposta ou evento | 🟢 |
| `projects/views.py:82` | API/worker/model conforme fonte | entidade, resposta ou evento | 🟢 |

## Fluxo Principal

1. Form válido chama get_or_create(name, owner); detalhe filtra nome+owner e inclui temp_dir/UUID; exclusão exige POST. 🟢
2. Atualizar estado e devolver resultado ao consumidor. 🟢

## Fluxos Alternativos

- **Falha:** Form inválido reaparece; recurso ausente/alheio retorna 404. 🟢 🟢
- **Divergência do legado:** exclusão atual remove somente o registro. 🔴 Contrato alvo confirmado exige remover container e workspace. 🟢

## Dependências

- Django ModelForm/ORM, auth.User, UI da IDE 🟢

## Decisões de Design Identificadas

| Decisão | Evidência no código | Confiança |
|---|---|---|
| Preservar integração existente e serialização de estado. | `projects/forms.py:6` | 🟢 |
| Aplicar limites e fluxo de recursos declarados. | `projects/views.py:46` | 🟢 |

## Estado Interno

Estado durável fica no banco; estado transitório fica em processo/container conforme código citado. 🟢

## Observabilidade

Erros são logados nas fontes citadas; métricas distribuídas não foram encontradas. 🟢

## Riscos e Lacunas

- Exclusão deve acionar cleanup do container e diretório do workspace. 🟢 Confirmado pelo usuário; o legado atual remove apenas a linha do projeto.

