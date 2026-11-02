# Núcleo da plataforma, Design Técnico

## Interface

| Símbolo | Assinatura | Retorno | Observação |
|---------|-----------|---------|------------|
| `create_submission` | `(request, question_uuid)` | Redirect HTTP | Requer POST e login; cria submissão e agenda worker. |
| `run_submission_runner` | `(submission_uuid)` | status final | Carrega casos, executa até primeira falha e persiste resultado. |
| `SubmissionRunnerManager.exe` | `(lang, work_dir, input_content, expected_output_content, source_file_content)` | dict `status/output/log` | Seleciona executor por linguagem. |
| `compute_leaderboard` | `(group_name='all')` | lista de posições e XP | Cacheia por grupo. |
| `random_unresolved_question` | `(user)` | `Question` ou `None` | Exclui questões invisíveis e já resolvidas. |

As rotas HTTP do núcleo são montadas por `SendIT/urls.py` incluindo `core.urls`; a lista de caminhos está detalhada na unit filha de questões/submissões. 🟢

## Fluxo Principal

1. Usuário autenticado consulta a home e o Django agrega questões pendentes, conquistas e avaliações relacionadas a seus grupos (`core/views.py:home`). 🟢
2. O usuário envia código/linguagem para uma questão; a view bloqueia questão já resolvida e novas tentativas em 15 segundos, persiste `Submission` e agenda o worker (`core/views.py:create_submission`). 🟢
3. O worker busca casos de teste e invoca runner apropriado para cada um; para no primeiro resultado diferente de `OK` (`core/worker.py`). 🟢
4. Runner prepara arquivos temporários, executa compilação e programa em container limitado, compara saída quando existe expected output e remove os temporários/container (`core/submission_runner.py`). 🟢
5. Worker grava status, saída e log, que são consultados pelas views de status/detalhe. 🟢

## Fluxos Alternativos

- **Questão já resolvida ou tentativa nos 15 segundos anteriores:** redireciona para a questão sem persistir/enfileirar nova tentativa. 🟢
- **Falha de compilação, runtime, timeout ou diferença:** runner retorna status de erro e worker encerra os testes restantes. 🟢
- **Sem casos de teste:** o loop não executa e status permanece `Waiting`. 🟢
- **Erro não mapeado em `SubmissionRunner.run`:** devolve `InternalError`; esse valor não consta em `STATUS_CHOICES`. 🟢
- **Falha de banco ao buscar submissão no worker:** não há tratamento local observado. 🔴 comportamento de retry e estado da fila depende da configuração RQ.

## Dependências

- Django ORM e PostgreSQL: modelos, agregações e consultas SQL do ranking.
- Redis e django-rq: fila assíncrona de submissões.
- Docker Engine e imagens por linguagem: isolamento e execução.
- `django-storages`/S3: badges e arquivos associados a conquistas.
- `evaluation` e `statistics`: home e dados de avaliação/atividade.

## Decisões de Design Identificadas

| Decisão | Evidência no código | Confiança |
|---------|---------------------|-----------|
| Persistir tentativa antes do processamento assíncrono | `core/views.py:create_submission` | 🟢 |
| Isolar código em container com limites e rede desabilitada | `core/submission_runner.py:run_process` | 🟢 |
| Configurar imagens/runtime por linguagem | `core/submission_runner.py:IMAGE_VERSION_DICT` | 🟢 |
| Usar SQL PostgreSQL direto em métricas de perfil/ranking | `core/models.py:UserData.setup_cache`, `core/domain.py:get_leaderboard` | 🟢 |
| Migrar de subprocess local para Docker por segurança | commit Git `4bfb1bd1` | 🟡 motivo inferido pelo diff e título/contexto da mudança |

## Estado Interno

- `Submission` persiste status, código, linguagem, autor, questão, saída e log.
- `SubmissionRunner` mantém temporariamente caminhos de trabalho e última saída em memória; seus arquivos ficam em `/tmp` e são removidos ao final.
- `UserData` agrega estatísticas no momento da criação; `compute_leaderboard` usa cache Redis por grupo sem TTL declarado nesta chamada.

## Observabilidade

- Logger `SubmissionRunner` registra execução e etapas de arquivos/container; os logs acumulados são devolvidos ao worker e armazenados na submissão.
- `core/domain.py` registra eventos da geração semanal de conquista e erros capturados.
- Não há métricas/traces distribuídos identificados nessa unit. 🟢

## Riscos e Lacunas

- 🔴 No legado, `submission_status` consulta UUID sem checar autor/staff; contrato alvo confirmado exige filtro. 🟢
- 🟢 Regra alvo confirmada: zero casos finaliza como `OK`; o legado atual pode deixar `Waiting`.
- 🟡 A execução segura depende de configuração e isolamento do Docker Engine no ambiente operacional.
- 🔴 Regras de retry/falha permanente da fila precisam de validação na configuração RQ/deploy.
