# Avaliações temporizadas e pontuação, Requirements

## Visão Geral

Controla início/fim de avaliações e calcula a nota a partir das questões resolvidas corretamente no período. 🟢

## Responsabilidades

- Criar ou recuperar participação com nota inicial zero. 🟢
- Calcular e persistir pontuação. 🟢
- Validar intervalo das datas da participação. 🟢

## Regras de Negócio

- Disponibilidade usa limites estritos. 🟢
- Pontuação inclui questões com ao menos uma submissão OK no período. 🟢
- QuestionInfo atribui decimal de até 5 dígitos/2 casas. 🟢
- Não há constraint visível de participação única por avaliação/aluno; concorrência pode criar duplicatas. 🔴

## Requisitos Funcionais

| ID | Requisito | Prioridade | Critério de Aceite |
|---|---|---|---|
| RF-01 | Criar ou recuperar participação com nota inicial zero. 🟢 | Must | Chave funcional é avaliação + autor. |
| RF-02 | Calcular e persistir pontuação. 🟢 | Must | Soma pontos de questões com submissões OK no intervalo. |
| RF-03 | Validar intervalo das datas da participação. 🟢 | Should | Datas fora do intervalo geram DateTimeRangeError quando clean é executado. |

## Requisitos Não Funcionais

| Tipo | Requisito inferido | Evidência no código | Confiança |
|---|---|---|---|
| Segurança | Restringir acesso aos dados do usuário autenticado e proprietário. | `evaluation/models.py:39` | 🟢 |
| Performance | Preservar operações assíncronas/consultas e limites existentes. | `evaluation/models.py:96` | 🟢 |

## Critérios de Aceitação

```gherkin
# 🟢 Happy path
Dado avaliações temporizadas e pontuação válidos e usuário autenticado
Quando o usuário realiza o fluxo principal
Então A participação é criada/recuperada por avaliação e aluno; compute_score filtra submissões OK no intervalo, soma pontos por questão e salva score.

# 🟢 Falha
Dado condição inválida ou acesso a recurso não autorizado
Quando o usuário tenta executar a ação
Então Submissões fora dos limites estritos não contam; clean contém validação de datas, mas não é chamada automaticamente pelo save observado.
```

## Prioridade (MoSCoW)

| Requisito | MoSCoW | Justificativa |
|---|---|---|
| Criar ou recuperar participação com nota inicial zero. 🟢 | Must | Caminho central da unit. 🟢 |
| Calcular e persistir pontuação. 🟢 | Must | Resultado principal do domínio. 🟢 |
| Validar intervalo das datas da participação. 🟢 | Should | Importante para integridade/segurança. 🟡 |

## Rastreabilidade de Código

| Arquivo | Função / Classe | Cobertura |
|---|---|---|
| `evaluation/models.py` | regra ou operação | 🟢 |
| `evaluation/models.py` | regra ou operação | 🟢 |
| `evaluation/models.py` | regra ou operação | 🟢 |

## Decisões Confirmadas pelo Usuário

- O servidor deve impedir início e consulta da participação fora da janela da avaliação. 🟢 Confirmado em 2026-11-02; adicionar checagem temporal nas views, pois `assessment_start` atualmente não chama `is_available()`.
- A participação e as submissões usadas na nota são visíveis somente ao próprio aluno e a staff autorizado. 🟢 Confirmado em 2026-11-02; o detalhe atual não filtra pelo autor.

