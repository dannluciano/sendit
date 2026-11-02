# Projetos, Tarefas de Implementação

## Pré-requisitos

- [ ] Dependências em `design.md` disponíveis.
- [ ] Schema do módulo compatível.
- [ ] Configuração de autenticação documentada. 🔴

## Tarefas

- [ ] T-01, Implementar entidades e validações.
  - Origem no legado: `projects/models.py:12`
  - Critério de pronto: campos/regras atendem a `requirements.md`.
  - Confiança: 🟢
- [ ] T-02, Implementar fluxo principal.
  - Origem no legado: `projects/views.py:46`
  - Critério de pronto: sequência e resposta correspondem a `design.md`.
  - Confiança: 🟢
- [ ] T-03, Aplicar autorização e tratamento de erro.
  - Origem no legado: `projects/views.py:66`
  - Critério de pronto: acesso indevido não revela nem altera recurso.
  - Confiança: 🟡

## Tarefas de Teste

- [ ] TT-01, Testar fluxo feliz e persistência.
  - Origem no legado: `projects/models.py:12`
  - Critério de pronto: cenário Gherkin passa.
  - Confiança: 🟢
- [ ] TT-02, Testar recurso ausente e acesso cruzado.
  - Origem no legado: `projects/views.py:46`
  - Critério de pronto: resposta segura e sem efeito lateral.
  - Confiança: 🟡

## Tarefas de Migração de Dados

- [ ] TM-01, Aplicar migrations do módulo.
  - Origem no legado: `projects/migrations/`
  - Critério de pronto: constraints e relações existem no banco.
  - Confiança: 🟡

## Ordem Sugerida

1. Schema.
2. Serviços e fluxo principal.
3. Autorização e tratamento de falhas.
4. Testes.

## Lacunas Pendentes (🔴)

- Implementar cleanup de container/workspace na exclusão, conforme confirmação do usuário. 🟢

