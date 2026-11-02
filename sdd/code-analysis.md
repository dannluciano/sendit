# Análise do código — sendit

## Escopo e confiança

Análise estrutural e estática do código. 🟢 **CONFIRMADO** indica comportamento diretamente visível no código; 🟡 **INFERIDO** indica leitura provável dos nomes e dependências; 🔴 **LACUNA** marca comportamento que exige exploração adicional.

## `core` — plataforma de desafios e submissões

### Responsabilidade

O app concentra autenticação da plataforma e páginas principais, questões, casos de teste, submissões, processamento assíncrono, ranking e conquistas. A URL raiz inclui as rotas `core.urls` (`SendIT/urls.py`). 🟢

### Fluxo de submissão

1. A view `create_submission` (`core/views.py`) recebe o UUID da questão, cria uma `Submission` com usuário, código e linguagem, e a salva com status inicial `Waiting`.
2. A view envia `run_submission_runner` para a fila RQ, passando o UUID da submissão.
3. O worker carrega submissão e casos de teste (`core/worker.py`), executa cada caso por meio do runner e persiste o resultado final, saída e log.
4. A consulta de status/resultado usa UUID; `Submission.get_absolute_url` distingue submissões ainda aguardando das concluídas.

### Execução isolada

`SubmissionRunnerManager` seleciona uma classe para C, C++, JavaScript, Java ou Python. Cada runner prepara arquivos temporários e usa a imagem correspondente (`core/submission_runner.py`). O container é executado sem rede, com limite de memória de 512 MB, 2 CPUs, 64 PIDs, sem novas permissões, sem capabilities e com filesystem somente leitura. O timeout padrão é 4 segundos, aumentado em 2 segundos para Java. Ao final, o container é removido e a pasta temporária apagada. 🟢

A compilação/validação e a execução são etapas distintas. Falhas são mapeadas para erro de sintaxe, execução, timeout ou diferença de saída; diferenças usam `difflib.unified_diff` comparando linhas. A saída capturada é truncada a 10.000 caracteres. 🟢

### Dados e regras

Entidades centrais: `Question`, `CaseTest`, `Submission`, `Tags`, `Achievement` e `AchievementPicture`, além de `auth.User`. XP padrão de questão/conquista é 100; a conquista pode ficar oculta. `Question` tem UUID único e visibilidade; `Submission` mantém linguagem, status, código, saída e log. 🟢

O ranking soma XP de submissões com status `OK` e XP de conquistas, calcula nível como raiz quadrada do XP de questões multiplicada por 1,5 (teto 74), remove grupo `Staff` e permite filtro por grupo. O resultado formatado é cacheado por chave `leaderboard-<grupo>` sem expiração explícita neste fluxo. O ranking semanal considera submissões corretas no intervalo da semana anterior e entrega uma conquista aos três primeiros usuários. 🟢

`random_unresolved_question` exclui questões invisíveis e questões já resolvidas pelo usuário, depois ordena aleatoriamente. 🟢 Ao submeter, usuários autenticados não podem reenviar questão já resolvida e novas submissões na mesma questão em janela inferior a 15 segundos são redirecionadas sem criar fila. 🟢

### Lacunas

- 🟢 O worker percorre os casos em ordem do queryset, encerra no primeiro resultado diferente de `OK` e grava apenas o último status/log/saída. Se a questão não tiver casos, o status inicial permanece `Waiting`; confirmar se esse cenário é permitido no domínio.
- 🔴 Semântica de segurança operacional dos containers depende também da configuração Docker e do ambiente de deploy.
- 🟡 `UserData` agrega dados via SQL PostgreSQL específico; dependência de portabilidade para outros bancos é provável, mas não é requisito declarado.

### Tabela resumida de dados

| Entidade | Campos principais |
|---|---|
| Question | título, enunciado, entrada/saída de exemplo, XP, tags, visibilidade, UUID |
| CaseTest | questão, entrada, saída esperada |
| Submission | UUID, autor, questão, código, status, timestamp, linguagem, log, saída |
| Achievement | nome, badge, XP, usuários, flag hidden |
| Tags | tag |
| AchievementPicture | bytes, filename, mimetype |

## Outros módulos

## `evaluation` — avaliações com prazo e pontuação

`Assessment` associa turmas/grupos a questões e a uma janela (`date_start`, `date_end`). A disponibilidade usa comparação estrita (`date_start < agora < date_end`), logo os limites exatos são indisponíveis. `QuestionInfo` associa uma questão à avaliação com pontuação decimal. `AssessmentSubmission` representa participação do aluno e guarda nota e datas. 🟢

As views autenticadas mostram detalhes, criam/recuperam a participação com nota inicial zero e calculam questões corretas com submissões cujo timestamp esteja estritamente entre o início e o fim. A nota soma os pontos das questões correspondentes e é persistida. A validação de data existe em `clean()`, mas a chamada de `full_clean()` não aparece no fluxo observado; não se deve presumir que seja aplicada automaticamente ao salvar. 🟢

**Lacuna:** `assessment_submission_detail` busca pelo UUID sem verificar que o autor da participação é o usuário autenticado; confirmar se há proteção em camada externa. 🟢 (ausência confirmada nesta view). `DateTimeRangeError` referencia `submission.start_at`, atributo não declarado em `AssessmentSubmission`, se a condição inválida for acionada. 🟢

## `editor` — execução avulsa e arquivos de código

`Runner` armazena UUID, código, linguagem, entrada, saída, status, log e timestamp. `FileCode` guarda UUID, nome, código, linguagem, datas e proprietário. A view de execução requer login e POST JSON (`code`, `lang`, `input`), cria um runner, agenda `run_submission_from_editor` via RQ e retorna UUID. O worker usa o mesmo `SubmissionRunnerManager` do módulo `core`, sem saída esperada, e atualiza o registro. 🟢

Salvar arquivo usa `update_or_create` por `(name, owner)`; a listagem filtra pelo usuário atual. Porém detalhe, download, exclusão e consulta do runner autenticam o usuário, mas não filtram o registro pelo proprietário. O caminho de download também indexa um mapa de extensões pela linguagem sem fallback. 🟢

**Lacuna:** o tratamento de erro de `create_runner` para JSON inválido/linguagem inválida não é explícito no código da view. 🔴

## `projects` — projetos pessoais e IDE baseada em containers

`Project` liga nome e proprietário, tem UUID, metadados de criação/atualização e `container_id`; uma constraint impede nomes repetidos por proprietário. O nome aceita apenas letras ASCII, números, `_` e `-`. As views exigem login, listam projetos do usuário e filtram detalhes/exclusão pelo proprietário. A criação usa `get_or_create(name, owner)`. 🟢

O detalhe serializa UUID, nome, owner_id, diretório temporário baseado no UUID e timestamps, além de detectar ícone de navegador pelo user agent. A integração com o serviço de containers é aprofundada em `projects-api`. 🟢

## `statistics` — atividade e métricas

`LogRecord` guarda usuário por username, check-in, check-out opcional e IP. Um signal cria o registro no login e, no logout, atualiza o último registro com hora e IP. `LastActivityMiddleware`, depois de cada resposta 200 não estática de usuário autenticado, atualiza o último registro com horário atual e IP. Quando há `X-Forwarded-For`, o valor completo é usado sem extração do primeiro endereço. 🟢

O app declara modelos somente leitura (`managed=False`) para views SQL de ranking, estatísticas e contagem de submissões. As consultas calculam XP/nível, taxas de conclusão/sucesso/erros e contagem por status. Dependem de sintaxe PostgreSQL (filtros agregados, `::`, funções de janela). 🟢

**Lacuna:** o middleware atualiza o registro mais recente em qualquer resposta elegível; detalhes de duração e interpretação de sessão dependem dessa sequência de sinais e requisições. 🔴

## `projects-api` — serviço Node para ambientes da IDE

O serviço Node/Hono escuta em `PORT` (padrão 8001), conecta ao Docker Engine pelo socket Unix, procura ou constrói a imagem `sendit-vm` no boot e expõe rotas HTTP e WebSocket. As rotas `/api/*` usam logger, autenticação por cookie `sessionid` assinado e CORS; `/version` fica fora desses middlewares. 🟢

`POST /api/container/create/` recebe `settings` e `project`, prepara diretório temporário, converte configurações em variáveis de ambiente, cria e inicia container com imagem VM, bind mount, TTY, porta 8080, 512 MB e limites de arquivos. Em produção define limite de storage de 2 GB. O estado do ambiente é mantido em Maps em memória, indexado por ID do container e do projeto, sem persistência após reinício. 🟢

O WebSocket `/vmws` liga cliente ao ambiente: envia árvore de arquivos e porta publicada ao receber `loaded`, suporta resize, escrita, criação de diretório e abertura de arquivo. Na desconexão para o container. Um segundo proxy `/containers/...` encaminha tráfego WebSocket ao Docker socket. 🟢

**Lacunas e riscos observados:** 🟢 o upgrade WebSocket não aplica o middleware HTTP de autenticação; várias mensagens (`mkdir`, `open`) não verificam proprietário. A escrita `writeInPath` compara `ownerUUID`, mas aceita o caminho fornecido pelo cliente. A rota de abrir arquivo concatena caminho decodificado ao diretório temporário sem validação de confinamento. O cookie secret possui fallback fixo no código. A autorização por cookie identifica sessão, mas não foi encontrado neste serviço vínculo explícito entre sessão e proprietário do projeto. 🔴 confirmar proteção em proxy ou em outras camadas.

## Resumo de entidades e dependências

Entidades principais do Django: `Question`, `CaseTest`, `Submission`, `Achievement`, `Assessment`, `QuestionInfo`, `AssessmentSubmission`, `Runner`, `FileCode`, `Project`, `LogRecord` e views de métricas. O serviço Node mantém representações `ComputerUnit` serializadas em memória e usa dados do projeto vindos do Django. 🟢

Dependências entre módulos: `evaluation` e `editor` dependem de `core`; `projects` integra com `projects-api`; `statistics` consulta tabelas de `core` e autenticação. Infraestrutura compartilhada: PostgreSQL, Redis/RQ, Docker e armazenamento S3/MinIO.

## Regras alvo validadas pelo usuário

Na revisão, o usuário confirmou que submissões sem casos devem ser `OK`; avaliações só podem ser iniciadas/consultadas dentro do período e por aluno dono/staff; status de submissão é restrito a autor/staff; arquivos e runners a owner/staff; WebSockets devem validar sessão/propriedade e confinar paths ao workspace; e excluir projeto deve remover container e workspace. 🟢

Essas decisões completam lacunas da análise e, em alguns pontos, diferem do comportamento atual descrito acima. As specs marcadas com a confirmação registram o contrato desejado sem afirmar que a implementação legada já o cumpre.
