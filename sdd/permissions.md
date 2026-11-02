# Matriz de permissões observada

| Recurso/ação | Visitante | Usuário autenticado | Staff/admin | Observação |
|---|---|---|---|---|
| Home, questões e ranking | Redirecionado para login | Acesso às áreas autenticadas | Acesso como usuário autenticado | Questões resolvidas e avaliações variam por usuário/grupo. |
| Criar submissão | Não | Sim, para própria conta | Sim | POST e janela anti-reenvio de 15s. |
| Ver detalhe da submissão | Não | Autor | Staff pode ver submissão de outro autor | `submission_status` aceita UUID sem checar autor. |
| Participação em avaliação | Não | Autenticado; associação a grupo é usada para listar avaliações | Autenticado | `assessment_submission_detail` não checa proprietário/autor. |
| Projetos | Não | CRUD do próprio projeto | Mesmo filtro por proprietário | Views filtram por owner. |
| Arquivos de código/Runner do editor | Não | CRUD/consulta requer login | Mesmo comportamento | Detalhe, download, exclusão e consulta Runner não filtram por proprietário. |
| Django Admin | Não | Conforme permissões Django | Staff/superuser conforme configuração Django | Grupo `Staff` do ranking não é necessariamente equivalente a `is_staff`; não inferir equivalência. |
| API HTTP `/api/*` da IDE | Redirecionado ao login sem cookie assinado | Cookie `sessionid` assinado aceito | Idem | Serviço Node guarda o valor como user-uuid; autorização de projeto não é comprovada. |
| WebSocket `/vmws` e proxy Docker | Não há middleware HTTP observado no upgrade | Não há validação explícita da sessão no handler | Não há distinção observada | Escritas `write`/`writeInPath` conferem ownerUUID em parte; `mkdir`/`open` não conferem. |

## Papéis observados

- **Visitante:** views decoradas com `login_required` encaminham ao login.
- **Usuário autenticado:** trabalha com submissões próprias e projetos próprios; várias views do editor e algumas views por UUID só exigem autenticação.
- **Staff (`is_staff`):** pode consultar detalhes de submissões de outros usuários e acessar perfil administrativo customizado.
- **Grupos Django:** associados a usuários e avaliações, e usados como filtro de ranking. O grupo de nome `Staff` é excluído do ranking.
- **Superuser/admin:** segue o sistema de permissões do Django Admin; a matriz de permissões específicas por model requer leitura aprofundada da configuração administrativa.

## Divergências de autorização no legado

As políticas alvo estão confirmadas na seção seguinte. Os itens abaixo descrevem diferenças de implementação ainda presentes no código legado:

1. 🔴 `submission_status` expõe status por UUID sem checagem de autor/staff.
2. 🔴 Views de `evaluation` por UUID não restringem participação ao autor nem aplicam sempre a janela temporal.
3. 🔴 Views do app `editor` exigem login, mas não confirmam proprietário.
4. 🔴 WebSockets não usam middleware HTTP; upgrades e comandos não validam sessão/owner/path de forma uniforme.
5. 🔴 O middleware da API verifica assinatura de cookie, mas não demonstra resolução da sessão Django nem autorização do usuário sobre o projeto recebido.

## Políticas alvo confirmadas pelo usuário

| Recurso | Política alvo confirmada | Divergência observada no legado |
|---|---|---|
| Status de submissão | Autor e staff autorizado | `submission_status` não filtra por autor/staff. |
| Participação em avaliação | Aluno dono ou staff autorizado; somente dentro da janela ativa | Views por UUID não filtram autoria nem checam a janela em todas as rotas. |
| Arquivos e runners do editor | Owner e staff autorizado | Views por UUID exigem login, mas não conferem owner. |
| WebSocket da IDE | Sessão Django válida, owner do projeto validado em cada operação e caminhos confinados ao workspace | Upgrade não passa pelo middleware HTTP; validação de owner/path é parcial. |
| Exclusão de projeto | Parar/remover container e apagar workspace | View Django remove apenas o registro `Project`. |

As políticas acima foram confirmadas pelo usuário em 2026-11-02. Elas descrevem o contrato alvo das specs, não o comportamento já implementado.
