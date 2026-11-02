# Ranking e conquistas, Tarefas de Implementação

## Pré-requisitos

- [ ] Dependências de `design.md` disponíveis.
- [ ] Schema compatível com entidades e relações legadas.
- [ ] Configuração/secrets documentados. 🔴

## Tarefas

- [ ] T-01, Implementar entidades e regras centrais.
  - Origem no legado: `core/domain.py:45`
  - Critério de pronto: dados e regras de `requirements.md` persistidos.
  - Confiança: 🟢
- [ ] T-02, Implementar fluxo e integrações.
  - Origem no legado: `core/domain.py:136`
  - Critério de pronto: fluxo principal corresponde a `design.md`.
  - Confiança: 🟢
- [ ] T-03, Implementar falhas e autorização do fluxo.
  - Origem no legado: `core/domain.py:220`
  - Critério de pronto: falha explícita e sem exposição não autorizada de dados.
  - Confiança: 🟡

## Tarefas de Teste

- [ ] TT-01, Testar cenário feliz de ponta a ponta.
  - Origem no legado: `core/domain.py:45`
  - Critério de pronto: resultado e persistência atendem ao Gherkin.
  - Confiança: 🟢
- [ ] TT-02, Testar erro principal e recurso ausente.
  - Origem no legado: `core/domain.py:136`
  - Critério de pronto: falha não deixa estado parcial inválido.
  - Confiança: 🟢

## Tarefas de Migração de Dados

- [ ] TM-01, Aplicar/verificar migrações do módulo.
  - Origem no legado: `core/migrations/`
  - Critério de pronto: schema reproduz entidades e relações necessárias.
  - Confiança: 🟡

## Ordem Sugerida

1. Schema/modelos.
2. Lógica de domínio e serviço.
3. Interface, integrações e autorização.
4. Testes de sucesso e falha.

## Lacunas Pendentes (🔴)

- TTL e invalidação de cache não são definidos no fluxo observado. 🔴

