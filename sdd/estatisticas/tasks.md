# Estatísticas, Tarefas de Implementação

## Pré-requisitos

- [ ] Dependências em `design.md` disponíveis.
- [ ] Schema/volume/serviços compatíveis.
- [ ] Segredos e ambiente documentados. 🔴

## Tarefas

- [ ] T-01, Implementar entidades/configuração/validação da unit.
  - Origem no legado: `statistics/models.py:13`
  - Critério de pronto: requisitos e limites declarados são aplicados.
  - Confiança: 🟢
- [ ] T-02, Implementar fluxo principal e integração.
  - Origem no legado: `statistics/domain.py:9`
  - Critério de pronto: consumidor recebe contrato descrito no design.
  - Confiança: 🟢
- [ ] T-03, Implementar autorização, cleanup e falhas.
  - Origem no legado: `statistics/middleware.py:10`
  - Critério de pronto: acesso não autorizado bloqueado e recursos liberados/recuperados.
  - Confiança: 🟡

## Tarefas de Teste

- [ ] TT-01, Testar caminho feliz e estado resultante.
  - Origem no legado: `statistics/models.py:13`
  - Critério de pronto: saída/registro corresponde ao Gherkin.
  - Confiança: 🟢
- [ ] TT-02, Testar falha de dependência e acesso cruzado.
  - Origem no legado: `statistics/domain.py:9`
  - Critério de pronto: erro é seguro e não deixa recursos órfãos.
  - Confiança: 🟡

## Tarefas de Migração de Dados

- [ ] TM-01, Confirmar migrations/estado do serviço antes da migração.
  - Origem no legado: `statistics/migrations/`
  - Critério de pronto: dados e referências permanecem válidos.
  - Confiança: 🟡

## Ordem Sugerida

1. Configuração e schema.
2. Fluxo de domínio e integração.
3. Autorização, erros e cleanup.
4. Testes dos caminhos principal e de falha.

## Lacunas Pendentes (🔴)

- Sessões simultâneas e confiança no proxy para X-Forwarded-For não estão definidas. 🔴

