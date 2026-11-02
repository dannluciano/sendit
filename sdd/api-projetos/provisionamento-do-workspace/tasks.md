# Provisionamento do workspace, Tarefas de Implementação

## Pré-requisitos

- [ ] Dependências em `design.md` disponíveis.
- [ ] Schema/volume/serviços compatíveis.
- [ ] Segredos e ambiente documentados. 🔴

## Tarefas

- [ ] T-01, Implementar entidades/configuração/validação da unit.
  - Origem no legado: `projects-api/api/computer_unit/computer_unit_controller.js:13`
  - Critério de pronto: requisitos e limites declarados são aplicados.
  - Confiança: 🟢
- [ ] T-02, Implementar fluxo principal e integração.
  - Origem no legado: `projects-api/api/computer_unit/computer_unit_service.js:12`
  - Critério de pronto: consumidor recebe contrato descrito no design.
  - Confiança: 🟢
- [ ] T-03, Implementar autorização, cleanup e falhas.
  - Origem no legado: `projects-api/api/computer_unit/temp_dir.js:11`
  - Critério de pronto: acesso não autorizado bloqueado e recursos liberados/recuperados.
  - Confiança: 🟡

## Tarefas de Teste

- [ ] TT-01, Testar caminho feliz e estado resultante.
  - Origem no legado: `projects-api/api/computer_unit/computer_unit_controller.js:13`
  - Critério de pronto: saída/registro corresponde ao Gherkin.
  - Confiança: 🟢
- [ ] TT-02, Testar falha de dependência e acesso cruzado.
  - Origem no legado: `projects-api/api/computer_unit/computer_unit_service.js:12`
  - Critério de pronto: erro é seguro e não deixa recursos órfãos.
  - Confiança: 🟡

## Tarefas de Migração de Dados

Não se aplica: a API não declara migrations ou banco próprio. Planejar recuperação do estado efêmero somente se for requisito confirmado. 🔴

## Ordem Sugerida

1. Configuração e schema.
2. Fluxo de domínio e integração.
3. Autorização, erros e cleanup.
4. Testes dos caminhos principal e de falha.

## Lacunas Pendentes (🔴)

- Restauração de ambientes após restart não está coberta. 🔴 Cleanup ao excluir projeto foi confirmado pelo usuário. 🟢

- [ ] T-04, Expor e integrar cleanup do container e diretório ao ciclo de exclusão de projeto.
  - Origem no legado: `projects-api/api/computer_unit/computer_unit_service.js:87`, `projects/views.py:82`
  - Critério de pronto: excluir projeto remove container e arquivos associados, reportando falhas de cleanup.
  - Confiança: 🟢 política confirmada pelo usuário em 2026-11-02.

