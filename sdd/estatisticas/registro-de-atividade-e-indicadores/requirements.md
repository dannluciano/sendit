# Registro de atividade e indicadores, Requirements

## Visão Geral

Mantém check-in/check-out/IP e calcula taxas agregadas por usuário e status de submissão. 🟢

## Responsabilidades

- Login cria LogRecord; navegação atualiza check_out/IP; views SQL calculam XP, nível, taxas e contagens. 🟢
- Taxas protegem divisões por zero; LogRecord identifica usuário pelo username. 🟢

## Regras de Negócio

- Taxas protegem divisões por zero; LogRecord identifica usuário pelo username. 🟢
- Sem registro aberto, set_last_activity não insere; SQL depende de sintaxe PostgreSQL. 🟢
- IP forwarded e concorrência de múltiplas sessões precisam definição. 🔴

## Requisitos Funcionais

| ID | Requisito | Prioridade | Critério de Aceite |
|---|---|---|---|
| RF-01 | Implementar fluxo principal desta unit. 🟢 | Must | Login cria LogRecord; navegação atualiza check_out/IP; views SQL calculam XP, nível, taxas e contagens. |
| RF-02 | Persistir/consultar estado e integração descrita. 🟢 | Must | Resultado corresponde aos campos e relações documentados. |
| RF-03 | Tratar falha e validar autorização. 🟡 | Must | Sem registro aberto, set_last_activity não insere; SQL depende de sintaxe PostgreSQL. 🟢 |

## Requisitos Não Funcionais

| Tipo | Requisito inferido | Evidência no código | Confiança |
|---|---|---|---|
| Segurança | Validar sessão, owner e caminho antes de acesso. | `statistics/models.py:13` | 🟢 |
| Performance | Preservar limites, SQL/debounce/integração já declarados. | `statistics/domain.py:22` | 🟢 |

## Critérios de Aceitação

```gherkin
# 🟢 Happy path
Dado usuário e dados válidos
Quando executa o fluxo principal
Então Login cria LogRecord; navegação atualiza check_out/IP; views SQL calculam XP, nível, taxas e contagens.

# 🟢 Falha
Dado recurso ausente ou usuário sem autorização
Quando solicita a operação
Então Sem registro aberto, set_last_activity não insere; SQL depende de sintaxe PostgreSQL. 🟢
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
| `statistics/models.py` | implementação descrita | 🟢 |
| `statistics/models.py` | implementação descrita | 🟢 |

