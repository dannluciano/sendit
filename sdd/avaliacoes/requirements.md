# Avaliações, Requirements

## Visão Geral

Agrupa questões pontuadas para turmas em uma janela temporal e apresenta a participação/resultados dos estudantes. 🟢

## Responsabilidades

- Manter avaliações, grupos, questões e pontuação. 🟢
- Exibir participação do aluno na avaliação. 🟢
- Bloquear início/consulta fora da janela e restringir autoria a aluno proprietário/staff. 🟢 Confirmado pelo usuário; legado diverge.

## Regras de Negócio

- Assessment associa grupos e questões via QuestionInfo com pontos decimais. 🟢
- Avaliação disponível somente se início < agora < fim. 🟢
- Views de participação requerem login. 🟢
- O servidor deve impedir início e consulta de participação fora da janela e permitir acesso apenas ao próprio aluno ou staff autorizado. 🟢 Confirmado pelo usuário; o legado não valida essas condições em todas as views.
- Legado não aplica checagem temporal em `assessment_start` nem filtra autoria no detalhe UUID. 🔴; o contrato alvo confirmado exige as duas verificações. 🟢

## Requisitos Funcionais

| ID | Requisito | Prioridade | Critério de Aceite |
|---|---|---|---|
| RF-01 | Manter avaliações, grupos, questões e pontuação. 🟢 | Must | Entidades e relações refletem período e pontos. |
| RF-02 | Exibir participação do aluno na avaliação. 🟢 | Must | Detalhe lista questões e submissões OK do usuário. |
| RF-03 | Aplicar controle de autoria e janela em todas as rotas de participação. 🟢 | Must | Só aluno dono/staff autorizado consulta durante período ativo. |

## Requisitos Não Funcionais

| Tipo | Requisito inferido | Evidência no código | Confiança |
|---|---|---|---|
| Segurança | Restringir acesso aos dados do usuário autenticado e proprietário. | `evaluation/models.py:13` | 🟢 |
| Performance | Preservar operações assíncronas/consultas e limites existentes. | `evaluation/views.py:10` | 🟢 |

## Critérios de Aceitação

```gherkin
# 🟢 Happy path
Dado avaliações válidos e usuário autenticado
Quando o usuário realiza o fluxo principal
Então Usuário autenticado consulta avaliações dos seus grupos dentro do período; inicia participação e acompanha questões corretas e pontuação.

# 🟢 Falha
Dado condição inválida ou acesso a recurso não autorizado
Quando o usuário tenta executar a ação
Então UUID inválido retorna não encontrado; acesso por UUID de outro aluno é negado, exceto a staff autorizado.
```

## Prioridade (MoSCoW)

| Requisito | MoSCoW | Justificativa |
|---|---|---|
| Manter avaliações, grupos, questões e pontuação. 🟢 | Must | Caminho central da unit. 🟢 |
| Exibir participação do aluno na avaliação. 🟢 | Must | Resultado principal do domínio. 🟢 |
| Controle de autoria e janela temporal | Must | Política de acesso confirmada pelo usuário. 🟢 |

## Rastreabilidade de Código

| Arquivo | Função / Classe | Cobertura |
|---|---|---|
| `evaluation/models.py` | regra ou operação | 🟢 |
| `evaluation/views.py` | regra ou operação | 🟢 |
| `evaluation/views.py` | regra ou operação | 🟢 |

