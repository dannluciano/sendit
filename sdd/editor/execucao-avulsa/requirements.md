# Execução avulsa do editor, Requirements

## Visão Geral

Executa código enviado pelo editor com entrada fornecida, sem comparação com saída esperada e sem vínculo a questão. 🟢

## Responsabilidades

- Criar execução com código, linguagem e stdin. 🟢
- Executar e armazenar resultado. 🟢
- Consultar status/saída pelo UUID. 🟢

## Regras de Negócio

- Requer login e POST para criar Runner. 🟢
- Execução não informa expected output, portanto não compara resultado. 🟢
- Runner segue status choices herdados de Submission. 🟢
- Consulta de Runner deve restringir resultado ao proprietário e a staff autorizado. 🟢 Confirmado pelo usuário em 2026-11-02; o legado atual não filtra owner.

## Requisitos Funcionais

| ID | Requisito | Prioridade | Critério de Aceite |
|---|---|---|---|
| RF-01 | Criar execução com código, linguagem e stdin. 🟢 | Must | POST cria registro Waiting e job RQ. |
| RF-02 | Executar e armazenar resultado. 🟢 | Must | Worker atualiza output/status/log. |
| RF-03 | Consultar status/saída pelo UUID. 🟢 | Must | Consulta retorna os campos ou 404. |

## Requisitos Não Funcionais

| Tipo | Requisito inferido | Evidência no código | Confiança |
|---|---|---|---|
| Segurança | Restringir acesso aos dados do usuário autenticado e proprietário. | `editor/views.py:28` | 🟢 |
| Performance | Preservar operações assíncronas/consultas e limites existentes. | `editor/views.py:48` | 🟢 |

## Critérios de Aceitação

```gherkin
# 🟢 Happy path
Dado execução avulsa do editor válidos e usuário autenticado
Quando o usuário realiza o fluxo principal
Então POST JSON cria Runner, agenda worker e responde UUID; worker executa linguagem via runner compartilhado e persiste status, saída e log.

# 🟢 Falha
Dado condição inválida ou acesso a recurso não autorizado
Quando o usuário tenta executar a ação
Então Runner inexistente é logado e ignorado pelo worker; linguagem inválida/JSON inválido não tem tratamento explícito na view.
```

## Prioridade (MoSCoW)

| Requisito | MoSCoW | Justificativa |
|---|---|---|
| Criar execução com código, linguagem e stdin. 🟢 | Must | Caminho central da unit. 🟢 |
| Executar e armazenar resultado. 🟢 | Must | Resultado principal do domínio. 🟢 |
| Consultar status/saída pelo UUID. 🟢 | Should | Importante para integridade/segurança. 🟡 |

## Rastreabilidade de Código

| Arquivo | Função / Classe | Cobertura |
|---|---|---|
| `editor/views.py` | regra ou operação | 🟢 |
| `editor/views.py` | regra ou operação | 🟢 |
| `editor/worker.py` | regra ou operação | 🟢 |

