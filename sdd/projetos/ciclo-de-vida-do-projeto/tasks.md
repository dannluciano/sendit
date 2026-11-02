# Ciclo de vida do projeto, Tarefas de Implementação

## Pré-requisitos

- [ ] Dependências em `design.md` disponíveis.
- [ ] Schema/volume/serviços compatíveis.
- [ ] Segredos e ambiente documentados. 🔴

## Tarefas

- [ ] T-01, Implementar entidades/configuração/validação da unit.
  - Origem no legado: `projects/forms.py:6`
  - Critério de pronto: requisitos e limites declarados são aplicados.
  - Confiança: 🟢
- [ ] T-02, Implementar fluxo principal e integração.
  - Origem no legado: `projects/views.py:46`
  - Critério de pronto: consumidor recebe contrato descrito no design.
  - Confiança: 🟢
- [ ] T-03, Implementar autorização, cleanup e falhas.
  - Origem no legado: `projects/models.py:54`
  - Critério de pronto: acesso não autorizado bloqueado e recursos liberados/recuperados.
  - Confiança: 🟡

## Tarefas de Teste

- [ ] TT-01, Testar caminho feliz e estado resultante.
  - Origem no legado: `projects/forms.py:6`
  - Critério de pronto: saída/registro corresponde ao Gherkin.
  - Confiança: 🟢
- [ ] TT-02, Testar falha de dependência e acesso cruzado.
  - Origem no legado: `projects/views.py:46`
  - Critério de pronto: erro é seguro e não deixa recursos órfãos.
  - Confiança: 🟡

## Tarefas de Migração de Dados

- [ ] TM-01, Confirmar migrations/estado do serviço antes da migração.
  - Origem no legado: `projects/migrations/`
  - Critério de pronto: dados e referências permanecem válidos.
  - Confiança: 🟡

## Ordem Sugerida

1. Configuração e schema.
2. Fluxo de domínio e integração.
3. Autorização, erros e cleanup.
4. Testes dos caminhos principal e de falha.

## Lacunas Pendentes (🔴)

- Política confirmada: excluir projeto deve remover container e workspace; legado atual não faz cleanup. 🟢

- [ ] T-04, Coordenar exclusão do registro Django, container Docker e diretório do workspace.
  - Origem no legado: `projects/views.py:82`, `projects-api/api/computer_unit/computer_unit_service.js:87`
  - Critério de pronto: após exclusão não existe projeto, container ativo nem diretório workspace residual.
  - Confiança: 🟢 confirmado pelo usuário em 2026-11-02.

