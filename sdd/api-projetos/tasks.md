# API de projetos, Tarefas de Implementação

## Pré-requisitos

- [ ] Dependências em `design.md` disponíveis.
- [ ] Schema/volume/serviços compatíveis.
- [ ] Segredos e ambiente documentados. 🔴

## Tarefas

- [ ] T-01, Implementar entidades/configuração/validação da unit.
  - Origem no legado: `projects-api/api/app.js:1`
  - Critério de pronto: requisitos e limites declarados são aplicados.
  - Confiança: 🟢
- [ ] T-02, Implementar fluxo principal e integração.
  - Origem no legado: `projects-api/api/routes.js:9`
  - Critério de pronto: consumidor recebe contrato descrito no design.
  - Confiança: 🟢
- [ ] T-03, Implementar autorização, cleanup e falhas.
  - Origem no legado: `projects-api/api/auth/auth_middleware.js:5`
  - Critério de pronto: acesso não autorizado bloqueado e recursos liberados/recuperados.
  - Confiança: 🟡

## Tarefas de Teste

- [ ] TT-01, Testar caminho feliz e estado resultante.
  - Origem no legado: `projects-api/api/app.js:1`
  - Critério de pronto: saída/registro corresponde ao Gherkin.
  - Confiança: 🟢
- [ ] TT-02, Testar falha de dependência e acesso cruzado.
  - Origem no legado: `projects-api/api/routes.js:9`
  - Critério de pronto: erro é seguro e não deixa recursos órfãos.
  - Confiança: 🟡

## Tarefas de Migração de Dados

Não se aplica: o serviço não declara migrations nem banco próprio. Seu estado de containers/socket fica em memória e os arquivos do workspace ficam em volume compartilhado. 🟢

## Ordem Sugerida

1. Configuração e schema.
2. Fluxo de domínio e integração.
3. Autorização, erros e cleanup.
4. Testes dos caminhos principal e de falha.

## Lacunas Pendentes (🔴)

- Upgrade WebSocket deve validar sessão e owner por operação conforme confirmação do usuário. 🟢

