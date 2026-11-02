# Estatísticas, Requirements

## Visão Geral

Registra atividade de sessão e expõe métricas de desempenho e submissões. 🟢

## Responsabilidades

- Signals criam/fecham LogRecord; middleware atualiza registro mais recente em respostas 200 autenticadas não estáticas; SQL views agregam submissões. 🟢
- Login cria log, logout fecha; métricas são modelos managed=False com SQL PostgreSQL. 🟢

## Regras de Negócio

- Login cria log, logout fecha; métricas são modelos managed=False com SQL PostgreSQL. 🟢
- Sem LogRecord anterior, atualização não cria; X-Forwarded-For é usado integralmente. 🟢
- Sessões simultâneas e confiança no proxy para X-Forwarded-For não estão definidas. 🔴

## Requisitos Funcionais

| ID | Requisito | Prioridade | Critério de Aceite |
|---|---|---|---|
| RF-01 | Implementar fluxo principal desta unit. 🟢 | Must | Signals criam/fecham LogRecord; middleware atualiza registro mais recente em respostas 200 autenticadas não estáticas; SQL views agregam submissões. |
| RF-02 | Persistir/consultar estado e integração descrita. 🟢 | Must | Resultado corresponde aos campos e relações documentados. |
| RF-03 | Tratar falha e validar autorização. 🟡 | Must | Sem LogRecord anterior, atualização não cria; X-Forwarded-For é usado integralmente. 🟢 |

## Requisitos Não Funcionais

| Tipo | Requisito inferido | Evidência no código | Confiança |
|---|---|---|---|
| Segurança | Validar sessão, owner e caminho antes de acesso. | `statistics/models.py:13` | 🟢 |
| Performance | Preservar limites, SQL/debounce/integração já declarados. | `statistics/domain.py:9` | 🟢 |

## Critérios de Aceitação

```gherkin
# 🟢 Happy path
Dado usuário e dados válidos
Quando executa o fluxo principal
Então Signals criam/fecham LogRecord; middleware atualiza registro mais recente em respostas 200 autenticadas não estáticas; SQL views agregam submissões.

# 🟢 Falha
Dado recurso ausente ou usuário sem autorização
Quando solicita a operação
Então Sem LogRecord anterior, atualização não cria; X-Forwarded-For é usado integralmente. 🟢
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
| `statistics/models.py` | implementação descrita | 🟢 |
| `statistics/domain.py` | implementação descrita | 🟢 |
| `statistics/middleware.py` | implementação descrita | 🟢 |
| `statistics/models.py` | implementação descrita | 🟢 |

