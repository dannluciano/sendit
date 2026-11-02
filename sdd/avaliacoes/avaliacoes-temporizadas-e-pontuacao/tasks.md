# Avaliações temporizadas e pontuação, Tarefas de Implementação

## Pré-requisitos

- [ ] Dependências descritas em `design.md` disponíveis.
- [ ] Schema compatível com modelos e relações.
- [ ] Configuração de filas/ambiente documentada. 🔴

## Tarefas

- [ ] T-01, Implementar entidades e regras de domínio.
  - Origem no legado: `evaluation/models.py:39`
  - Critério de pronto: campos, relações e defaults atendem `requirements.md`.
  - Confiança: 🟢
- [ ] T-02, Implementar fluxo principal e integrações.
  - Origem no legado: `evaluation/models.py:96`
  - Critério de pronto: operação de sucesso segue a sequência descrita em `design.md`.
  - Confiança: 🟢
- [ ] T-03, Implementar validação de falha e autorização de propriedade.
  - Origem no legado: `evaluation/models.py:147`
  - Critério de pronto: recurso ausente e acesso não autorizado não expõem dados.
  - Confiança: 🟡

## Tarefas de Teste

- [ ] TT-01, Testar fluxo principal e persistência.
  - Origem no legado: `evaluation/models.py:39`
  - Critério de pronto: cenário Gherkin de sucesso passa.
  - Confiança: 🟢
- [ ] TT-02, Testar erro principal e permissão.
  - Origem no legado: `evaluation/models.py:96`
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

## Regras de Acesso Confirmadas

- [ ] T-04, Validar janela ativa no início e na consulta da participação.
  - Origem no legado: `evaluation/models.py:39`, `evaluation/views.py:28`, `evaluation/views.py:46`
  - Critério de pronto: fora do período, início e consulta são negados; limites permanecem estritos.
  - Confiança: 🟢 confirmado pelo usuário em 2026-11-02.
- [ ] T-05, Filtrar participação por autor e permitir exceção somente a staff autorizado.
  - Origem no legado: `evaluation/views.py:46`
  - Critério de pronto: aluno não acessa UUID de outro aluno; staff autorizado pode consultar.
  - Confiança: 🟢 confirmado pelo usuário em 2026-11-02.

## Lacunas Pendentes (🔴)

- Não há constraint visível de participação única por avaliação/aluno; concorrência pode criar duplicatas. 🔴

