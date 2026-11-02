# Núcleo da plataforma, Tarefas de Implementação

## Pré-requisitos

- [ ] Dependências de Django, Redis/RQ e Docker Engine disponíveis conforme `../dependencies.md`.
- [ ] Schema compatível com as entidades centrais (`core/models.py` e migrações).
- [ ] Imagens de execução e variáveis de conexão documentadas para cada ambiente.

## Tarefas

- [ ] T-01, Implementar entidades centrais de questão, caso de teste, submissão, tag e conquista.
  - Origem no legado: `core/models.py:87`, `core/models.py:138`, `core/models.py:156`, `core/models.py:340`
  - Critério de pronto: campos, relações, defaults, choices, UUIDs e ordenações são representados e persistidos.
  - Confiança: 🟢

- [ ] T-02, Implementar páginas/rotas autenticadas de questões, submissões e ranking.
  - Origem no legado: `core/urls.py:1`, `core/views.py:62`, `core/views.py:213`, `core/views.py:251`
  - Critério de pronto: rotas resolvem recursos por ID/UUID e preservam os filtros de usuário, visibilidade e grupo documentados.
  - Confiança: 🟢

- [ ] T-03, Aplicar regras de criação e limitação de submissões.
  - Origem no legado: `core/views.py:213`
  - Critério de pronto: usuário autenticado não cria submissão duplicada após sucesso nem outra tentativa dentro da janela de 15 segundos.
  - Confiança: 🟢

- [ ] T-04, Implementar enfileiramento e processamento de submissões por casos de teste.
  - Origem no legado: `core/views.py:240`, `core/worker.py:5`
  - Critério de pronto: trabalho persiste status, log e saída, interrompendo no primeiro caso não aprovado.
  - Confiança: 🟢

- [ ] T-05, Implementar runner por linguagem em container isolado.
  - Origem no legado: `core/submission_runner.py:53`, `core/submission_runner.py:103`, `core/submission_runner.py:340`
  - Critério de pronto: compila/valida e executa com limites configurados; mapeia timeout, falha runtime e erro de sintaxe para resultado explícito.
  - Confiança: 🟢

- [ ] T-06, Implementar comparação da saída do programa com saída esperada.
  - Origem no legado: `core/submission_runner.py:184`
  - Critério de pronto: saída igual produz `OK`; diferença produz `DiffError` e preserva diff para consulta.
  - Confiança: 🟢

- [ ] T-07, Implementar perfil, seleção de questão pendente, XP, conquistas e ranking.
  - Origem no legado: `core/domain.py:97`, `core/domain.py:220`, `core/models.py:15`
  - Critério de pronto: perfil e ranking aplicam XP, nível, exclusão de Staff, conquistas e filtros por grupo descritos.
  - Confiança: 🟢

## Tarefas de Teste

- [ ] TT-01, Cobrir envio autenticado, enfileiramento e bloqueio por questão resolvida/janela de 15 segundos.
  - Origem no legado: `core/views.py:213`
  - Critério de pronto: cenários aceito e bloqueado verificam persistência e chamada à fila.
  - Confiança: 🟢
- [ ] TT-02, Cobrir status de compilação, runtime, timeout, diff e sucesso para os runners suportados.
  - Origem no legado: `core/submission_runner.py:103`, `core/submission_runner.py:184`
  - Critério de pronto: cada condição produz o status e a saída esperados sem deixar container/arquivos temporários ativos.
  - Confiança: 🟢
- [ ] TT-03, Cobrir processamento de zero, um e vários casos de teste.
  - Origem no legado: `core/worker.py:5`
  - Critério de pronto: primeiro erro interrompe execução; zero casos finaliza `OK`, conforme decisão confirmada; o legado diverge.
  - Confiança: 🟢 regra alvo confirmada pelo usuário em 2026-11-02.
- [ ] TT-04, Cobrir autorização de consulta de status por autor e staff.
  - Origem no legado: `core/views.py:296`, `core/views.py:309`
  - Critério de pronto: usuário não autorizado não consegue consultar status de submissão alheia.
  - Confiança: 🟡 requisito de segurança recomendado a partir da lacuna observada.

## Tarefas de Migração de Dados

- [ ] TM-01, Aplicar migrações existentes de `core` e migrações de autenticação dependentes.
  - Origem no legado: `core/migrations/`
  - Critério de pronto: schema de produção corresponde às entidades e índices/constraints esperados.
  - Confiança: 🟢

## Ordem Sugerida

1. Implementar entidades/migrações e validações.
2. Implementar execução e worker, pois submissão depende desse contrato.
3. Implementar rotas de questão e submissão sobre os serviços concluídos.
4. Implementar perfil, ranking e conquistas.
5. Validar permissões e comportamento de fila/containers por testes automatizados.

## Lacunas Pendentes (🔴)

- Implementar resultado `OK` para zero casos conforme decisão confirmada; o legado diverge. 🟢
- Definir política de retry e estado terminal quando o worker falha antes de persistir resultado.
- Confirmar se saídas de execução devem ter limite diferente dos 10.000 caracteres atualmente observados.
