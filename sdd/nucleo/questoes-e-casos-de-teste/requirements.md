# Questões e casos de teste, Requirements

## Visão Geral

Questões são desafios com enunciado, XP, tags, visibilidade e exemplos de entrada/saída. Cada questão pode ter vários casos de teste usados pelo worker para validar submissões. 🟢

## Responsabilidades

- Manter questões, tags e casos de teste. 🟢
- Apresentar questões visíveis ainda não resolvidas e permitir busca/filtro. 🟢
- Permitir administração para criar, editar, ocultar, exibir e associar casos de teste. 🟢

## Regras de Negócio

- Questões são ordenadas por título por padrão e têm XP padrão 100, visibilidade padrão verdadeira e UUID único. 🟢
- Questões invisíveis são removidas do catálogo da home e da seleção aleatória de questões pendentes. 🟢
- Questões já resolvidas (submissão `OK` do usuário) não são oferecidas no catálogo pendente. 🟢
- Busca aceita até 100 caracteres e remove pontuação/símbolos antes de filtrar título e enunciado. 🟢
- Casos de teste pertencem a uma questão e podem ter entrada/saída vazias. 🟢
- 🔴 Não foi identificada regra de validação para impedir questão sem casos de teste.

## Requisitos Funcionais

| ID | Requisito | Prioridade | Critério de Aceite |
|----|-----------|-----------|-------------------|
| RF-01 | Persistir questão com UUID, enunciado, título, XP, tags, exemplos e flag de visibilidade. 🟢 | Must | Questão criada apresenta defaults de XP e visibilidade e URL reversível pelo UUID. |
| RF-02 | Associar múltiplos casos de teste à questão. 🟢 | Must | Caso é recuperável pela questão e contém entrada/saída esperada. |
| RF-03 | Listar até dez questões visíveis e não resolvidas, ordenadas por XP. 🟢 | Must | Home não inclui questão invisível nem já concluída e limita resultado a dez. |
| RF-04 | Buscar por título/enunciado e filtrar por tag. 🟢 | Should | Filtros válidos refinam a lista; `tag=all` não restringe por tag. |
| RF-05 | Administrar visibilidade e casos de teste de questões. 🟢 | Should | Ações de admin alteram `visible`; inline permite manter casos vinculados. |
| RF-06 | Abrir detalhe por ID ou UUID para usuário autenticado. 🟢 | Should | ID requer questão visível; caminho por UUID retorna questão localizada. |

## Requisitos Não Funcionais

| Tipo | Requisito inferido | Evidência no código | Confiança |
|------|--------------------|---------------------|-----------|
| Segurança | Páginas do catálogo/detalhe exigem login; administração usa Django Admin. | `core/views.py:62`, `core/views.py:165`, `core/admin.py:52` | 🟢 |
| Performance | Home pré-carrega tags e limita a consulta a dez questões. | `core/views.py:73`, `core/views.py:93` | 🟢 |

## Critérios de Aceitação

```gherkin
# 🟢 Happy path
Dado um usuário autenticado e uma questão visível ainda não resolvida
Quando ele abre a home do SendIT
Então a questão aparece na lista pendente com tags e informação de XP

# 🟢 Falha/ocultação
Dado uma questão marcada como invisível
Quando um usuário abre a lista ou solicita o detalhe por ID
Então a questão não aparece na lista e o detalhe por ID não a retorna

# 🟢 Happy path de busca
Dado questões visíveis com títulos, enunciados e tags
Quando o usuário informa busca e tag válidas
Então o catálogo retorna apenas os resultados compatíveis, até o limite de dez

# 🟢 Caso de entrada inválida
Dado uma busca com mais de 100 caracteres
Quando o formulário é validado
Então a busca é rejeitada pelo limite do campo e não restringe silenciosamente o catálogo
```

## Prioridade (MoSCoW)

| Requisito | MoSCoW | Justificativa |
|-----------|--------|---------------|
| Questão e casos de teste | Must | Necessários para desafios e validação de código. 🟢 |
| Lista de questões pendentes | Must | Entrada principal para resolver exercícios. 🟢 |
| Busca e filtro por tag | Should | Facilita navegação, mas não bloqueia acesso por URL. 🟢 |
| Ações administrativas de visibilidade | Should | Moderação de conteúdo importante após publicação. 🟡 |

> Prioridade inferida por frequência de chamada e dependências.

## Rastreabilidade de Código

| Arquivo | Função / Classe | Cobertura |
|---------|-----------------|-----------|
| `core/models.py` | `Question`, `CaseTest`, `Tags` | 🟢 |
| `core/forms.py` | `QuestionSearchForm.clean_q` | 🟢 |
| `core/views.py` | `home`, `random_question`, `completed_issues`, `get_question` | 🟢 |
| `core/admin.py` | `QuestionAdmin`, `CaseTestInline`, ações `hide`/`show` | 🟢 |
