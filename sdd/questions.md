# Perguntas para Validação — sendit

> Gerado pelo Revisor e respondido pelo usuário em 2026-11-02. As respostas foram incorporadas às specs; o histórico fica aqui.

---

## Pergunta 1 — Questão sem casos de teste

**Contexto:** `core.worker.run_submission_runner` mantém o status inicial `Waiting` se a questão não tiver `CaseTest`.
**Spec afetada:** [`nucleo/submissao-e-avaliacao-de-codigo`](nucleo/submissao-e-avaliacao-de-codigo/requirements.md)
**Pergunta:** Qual deve ser o resultado de uma submissão para questão sem casos de teste: rejeitar configuração, aprovar, ou registrar um estado de erro específico?
**Impacto:** Define a transição terminal e evita submissões presas em `Waiting`.

✅ Respondida
**Resposta:** Aprovar

---

## Pergunta 2 — Início de avaliação fora do período

**Contexto:** `evaluation.views.assessment_start` cria/recupera participação sem chamar `Assessment.is_available`; as avaliações da home, porém, são filtradas pela janela de tempo.
**Spec afetada:** [`avaliacoes/avaliacoes-temporizadas-e-pontuacao`](avaliacoes/avaliacoes-temporizadas-e-pontuacao/requirements.md)
**Pergunta:** O servidor deve impedir início/consulta de participação fora da janela da avaliação, inclusive se o usuário chamar a URL diretamente?
**Impacto:** Determina a regra de autorização temporal para rotas de avaliação.

✅ Respondida
**Resposta:** Sim o servidor deve impedir o início/consulta de participação fora da janela da avaliação

---

## Pergunta 3 — Autoria da participação em avaliação

**Contexto:** `assessment_submission_detail` carrega uma participação pelo UUID sem comparar `assessment_submission.author` com o usuário autenticado.
**Spec afetada:** [`avaliacoes/avaliacoes-temporizadas-e-pontuacao`](avaliacoes/avaliacoes-temporizadas-e-pontuacao/requirements.md)
**Pergunta:** A participação e as submissões usadas na nota devem ser visíveis somente ao próprio aluno e a staff autorizado?
**Impacto:** Define o filtro de proprietário e o acesso administrativo ao detalhe da avaliação.

✅ Respondida
**Resposta:** Sim, A participação e as submissões usadas na nota devem ser visíveis somente ao próprio aluno e a staff autorizado.

---

## Pergunta 4 — Consulta do status de submissão

**Contexto:** `core.views.submission_status` aceita qualquer UUID encontrado para qualquer usuário autenticado; `submission_detail` aplica uma checagem de autor/staff.
**Spec afetada:** [`nucleo/submissao-e-avaliacao-de-codigo`](nucleo/submissao-e-avaliacao-de-codigo/requirements.md)
**Pergunta:** O status da submissão também deve ser restrito ao autor e staff, como o detalhe final?
**Impacto:** Define se UUIDs podem ser usados para consultar atividade de outros usuários.

✅ Respondida
**Resposta:** Sim

---

## Pergunta 5 — Propriedade dos arquivos e runners do editor

**Contexto:** `editor.views.file_code_detail`, download, destroy e `runner_details` exigem login, mas não filtram registros pelo proprietário.
**Spec afetada:** [`editor/arquivos-de-codigo`](editor/arquivos-de-codigo/requirements.md) e [`editor/execucao-avulsa`](editor/execucao-avulsa/requirements.md)
**Pergunta:** Arquivos e resultados do Runner devem ser acessíveis somente ao owner, com exceção de staff autorizado?
**Impacto:** Define filtros de consulta/alteração por owner e possíveis permissões administrativas.

✅ Respondida
**Resposta:** Sim

---

## Pergunta 6 — Autorização e caminhos do WebSocket da IDE

**Contexto:** O upgrade WebSocket não aplica o middleware HTTP de cookie; nem todas as mensagens validam `ownerUUID`, e caminhos de arquivo recebidos do cliente não são confinados ao workspace.
**Spec afetada:** [`api-projetos/filesystem-e-terminal-interativo`](api-projetos/filesystem-e-terminal-interativo/requirements.md)
**Pergunta:** A conexão WebSocket deve validar a sessão Django e propriedade do projeto antes de cada operação, e as operações de arquivo devem ficar confinadas ao workspace do projeto?
**Impacto:** Define o contrato de autenticação/autorização da IDE e a política de acesso ao filesystem.

✅ Respondida
**Resposta:** Sim

---

## Pergunta 7 — Exclusão de projeto e workspace

**Contexto:** A view de exclusão remove o registro `Project`; não há chamada visível para parar o container ou limpar o diretório host.
**Spec afetada:** [`projetos/ciclo-de-vida-do-projeto`](projetos/ciclo-de-vida-do-projeto/requirements.md) e [`api-projetos/provisionamento-do-workspace`](api-projetos/provisionamento-do-workspace/requirements.md)
**Pergunta:** Ao excluir um projeto, o sistema deve parar/remover seu container e apagar o workspace, preservá-lo ou solicitar confirmação?
**Impacto:** Define a política de retenção e limpeza de recursos e dados de usuário.

✅ Respondida
**Resposta:** Sim — ao excluir o projeto, parar/remover seu container e apagar o workspace.
