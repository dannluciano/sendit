# Editor, Requirements

## Visão Geral

Oferece execução independente de código e gerenciamento de arquivos de código do usuário pela interface web. 🟢

## Responsabilidades

- Executar código avulso e consultar seu resultado. 🟢
- Salvar e organizar arquivos de código. 🟢
- Restringir operações de arquivo ao proprietário. 🟡

## Regras de Negócio

- Runner reutiliza SubmissionRunnerManager do core. 🟢
- FileCode usa owner e nome para update_or_create. 🟢
- Views exigem login; no legado detalhe/download/exclusão não filtram owner. 🟢
- Política alvo confirmada: arquivos e Runners são acessíveis somente ao owner e a staff autorizado. 🟢 Confirmado pelo usuário em 2026-11-02.

## Requisitos Funcionais

| ID | Requisito | Prioridade | Critério de Aceite |
|---|---|---|---|
| RF-01 | Executar código avulso e consultar seu resultado. 🟢 | Must | POST retorna UUID e resultado inclui status/saída. |
| RF-02 | Salvar e organizar arquivos de código. 🟢 | Must | Arquivo é associado ao usuário e listagem ordenada por atualização. |
| RF-03 | Restringir operações de arquivo ao proprietário. 🟡 | Must | Usuário não acessa arquivo de outro owner. |

## Requisitos Não Funcionais

| Tipo | Requisito inferido | Evidência no código | Confiança |
|---|---|---|---|
| Segurança | Restringir acesso aos dados do usuário autenticado e proprietário. | `editor/models.py:10` | 🟢 |
| Performance | Preservar operações assíncronas/consultas e limites existentes. | `editor/views.py:28` | 🟢 |

## Critérios de Aceitação

```gherkin
# 🟢 Happy path
Dado editor válidos e usuário autenticado
Quando o usuário realiza o fluxo principal
Então Usuário autenticado executa código pela fila RQ e salva/lista/abre/baixa/exclui seus arquivos.

# 🟢 Falha
Dado condição inválida ou acesso a recurso não autorizado
Quando o usuário tenta executar a ação
Então Runner ou arquivo consultado por UUID sem correspondência resulta em 404 onde explicitamente tratado; ownership não é validado em várias views.
```

## Prioridade (MoSCoW)

| Requisito | MoSCoW | Justificativa |
|---|---|---|
| Executar código avulso e consultar seu resultado. 🟢 | Must | Caminho central da unit. 🟢 |
| Salvar e organizar arquivos de código. 🟢 | Must | Resultado principal do domínio. 🟢 |
| Restringir operações de arquivo ao proprietário. 🟡 | Should | Importante para integridade/segurança. 🟡 |

## Rastreabilidade de Código

| Arquivo | Função / Classe | Cobertura |
|---|---|---|
| `editor/models.py` | regra ou operação | 🟢 |
| `editor/views.py` | regra ou operação | 🟢 |
| `editor/worker.py` | regra ou operação | 🟢 |

