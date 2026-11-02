# Avaliações, Tarefas de Implementação

## Pré-requisitos

- [ ] Dependências descritas em `design.md` disponíveis.
- [ ] Schema compatível com modelos e relações.
- [ ] Configuração de filas/ambiente documentada. 🔴

## Tarefas

- [ ] T-01, Implementar entidades e regras de domínio.
  - Origem no legado: `evaluation/models.py:13`
  - Critério de pronto: campos, relações e defaults atendem `requirements.md`.
  - Confiança: 🟢
- [ ] T-02, Implementar fluxo principal e integrações.
  - Origem no legado: `evaluation/views.py:10`
  - Critério de pronto: operação de sucesso segue a sequência descrita em `design.md`.
  - Confiança: 🟢
- [ ] T-03, Implementar validação de falha e autorização de propriedade.
  - Origem no legado: `evaluation/views.py:28`
  - Critério de pronto: recurso ausente e acesso não autorizado não expõem dados.
  - Confiança: 🟡

## Tarefas de Teste

- [ ] TT-01, Testar fluxo principal e persistência.
  - Origem no legado: `evaluation/models.py:13`
  - Critério de pronto: cenário Gherkin de sucesso passa.
  - Confiança: 🟢
- [ ] TT-02, Testar erro principal e permissão.
  - Origem no legado: `evaluation/views.py:10`
  - Critério de pronto: falha não deixa estado inconsistente nem expõe dados alheios.
  - Confiança: 🟡

## Tarefas de Migração de Dados

- [ ] TM-01, Aplicar/verificar migrations do módulo.
  - Origem no legado: `evaluation/migrations/`
  - Critério de pronto: schema corresponde aos relacionamentos necessários.
  - Confiança: 🟡

## Ordem Sugerida

1. Models/schema e constraints.
2. Serviço e fluxo de domínio.
3. Endpoints, UI e autorização.
4. Testes de sucesso, falha e acesso.

## Lacunas Pendentes (🔴)

- Legado não aplica janela/autoria em todas as views; implementação alvo deve obedecer às regras confirmadas nesta spec. 🟢

