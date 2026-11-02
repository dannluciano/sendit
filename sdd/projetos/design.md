# Projetos, Design Técnico

## Interface

| Símbolo | Assinatura | Retorno | Observação |
|---|---|---|---|
| `projects/models.py:12` | funções do módulo | resposta/modelo | 🟢 |
| `projects/views.py:46` | funções do módulo | resposta/modelo | 🟢 |
| `projects/views.py:66` | funções do módulo | resposta/modelo | 🟢 |
| `projects/views.py:82` | funções do módulo | resposta/modelo | 🟢 |

## Fluxo Principal

1. Usuário cria projeto validado, lista próprios projetos, consulta detalhe serializado e exclui via POST. 🟢
2. Persistir alterações e retornar resultado ao consumidor. 🟢

## Fluxos Alternativos

- **Falha:** Form inválido é reexibido; projeto ausente/alheio não é encontrado. 🟢 🟢
- **Divergência do legado:** view exclui somente o registro. 🔴 Contrato alvo confirmado exige remover container e workspace. 🟢

## Dependências

- Django ModelForm/ORM, auth.User e projects-api 🟢

## Decisões de Design Identificadas

| Decisão | Evidência no código | Confiança |
|---|---|---|
| Usar ORM e chave de recurso observados no legado. | `projects/models.py:12` | 🟢 |
| Integrar com dependências atuais do módulo. | `projects/views.py:46` | 🟢 |

## Estado Interno

Estado durável é persistido nas entidades da unit. 🟢

## Observabilidade

Logs/métricas adicionais não identificados. 🟢

## Riscos e Lacunas

- Exclusão alvo remove container e workspace conforme confirmação do usuário; legado diverge. 🟢

