# Filesystem e terminal interativo, Tarefas de Implementação

## Pré-requisitos

- [ ] Dependências em `design.md` disponíveis.
- [ ] Schema/volume/serviços compatíveis.
- [ ] Segredos e ambiente documentados. 🔴

## Tarefas

- [ ] T-01, Implementar entidades/configuração/validação da unit.
  - Origem no legado: `projects-api/api/websocket/api_websocket.js:6`
  - Critério de pronto: requisitos e limites declarados são aplicados.
  - Confiança: 🟢
- [ ] T-02, Implementar fluxo principal e integração.
  - Origem no legado: `projects-api/api/websocket/docker_websocket.js:3`
  - Critério de pronto: consumidor recebe contrato descrito no design.
  - Confiança: 🟢
- [ ] T-03, Implementar autorização, cleanup e falhas.
  - Origem no legado: `projects-api/api/computer_unit/temp_dir.js:20`
  - Critério de pronto: acesso não autorizado bloqueado e recursos liberados/recuperados.
  - Confiança: 🟡

## Tarefas de Teste

- [ ] TT-01, Testar caminho feliz e estado resultante.
  - Origem no legado: `projects-api/api/websocket/api_websocket.js:6`
  - Critério de pronto: saída/registro corresponde ao Gherkin.
  - Confiança: 🟢
- [ ] TT-02, Testar falha de dependência e acesso cruzado.
  - Origem no legado: `projects-api/api/websocket/docker_websocket.js:3`
  - Critério de pronto: erro é seguro e não deixa recursos órfãos.
  - Confiança: 🟡

## Tarefas de Migração de Dados

Não se aplica: o serviço não declara migrations; arquivos ficam em workspace compartilhado e índices de conexão são mantidos em memória. 🟢

## Ordem Sugerida

1. Configuração e schema.
2. Fluxo de domínio e integração.
3. Autorização, erros e cleanup.
4. Testes dos caminhos principal e de falha.

## Lacunas Pendentes (🔴)

- Implementação alvo confirmada: autenticar sessão Django, validar owner em cada mensagem e canonicalizar/confinar caminhos ao workspace. 🟢

- [ ] T-04, Autenticar upgrades e autorizar cada operação WebSocket por usuário/projeto.
  - Origem no legado: `projects-api/api/app.js:43`, `projects-api/api/websocket/api_websocket.js:6`
  - Critério de pronto: sem sessão válida ou propriedade confirmada, operação é rejeitada.
  - Confiança: 🟢 política confirmada pelo usuário em 2026-11-02.
- [ ] T-05, Confinar caminhos de leitura/escrita ao diretório workspace canonicalizado.
  - Origem no legado: `projects-api/api/websocket/api_websocket.js:35`, `projects-api/api/projects/projects_controller.js:6`
  - Critério de pronto: traversal e caminhos fora do workspace são bloqueados.
  - Confiança: 🟢 política confirmada pelo usuário em 2026-11-02.

