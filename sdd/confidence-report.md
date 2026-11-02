# Relatório de Confiança — sendit

> Revisão concluída em 2026-11-02. Nível configurado: Essencial.

---

## Resumo Geral

Contagem dos marcadores de confiança presentes nos 51 arquivos canônicos das 17 units:

| Nível | Quantidade | Percentual |
|-------|-----------:|-----------:|
| 🟢 CONFIRMADO | 724 | 82,7% |
| 🟡 INFERIDO | 71 | 8,1% |
| 🔴 LACUNA | 80 | 9,1% |
| **Total de marcadores** | **875** | **100%** |

**Confiança geral:** **87%** — cálculo simplificado: (724 + 71 × 0,5) / 875. Os marcadores podem repetir uma mesma regra em requirements, design e tasks; a contagem não representa afirmações únicas.

## Por Unit

| Unit | 🟢 | 🟡 | 🔴 | Confiança |
|------|---:|---:|---:|---:|
| `sdd/api-projetos/` | 38 | 4 | 4 | 87% |
| `sdd/api-projetos/filesystem-e-terminal-interativo/` | 39 | 3 | 4 | 88% |
| `sdd/api-projetos/provisionamento-do-workspace/` | 37 | 4 | 7 | 81% |
| `sdd/avaliacoes/` | 45 | 3 | 5 | 88% |
| `sdd/avaliacoes/avaliacoes-temporizadas-e-pontuacao/` | 45 | 4 | 7 | 84% |
| `sdd/editor/` | 41 | 7 | 3 | 87% |
| `sdd/editor/arquivos-de-codigo/` | 39 | 4 | 2 | 91% |
| `sdd/editor/execucao-avulsa/` | 44 | 4 | 2 | 92% |
| `sdd/estatisticas/` | 35 | 5 | 6 | 82% |
| `sdd/estatisticas/registro-de-atividade-e-indicadores/` | 35 | 5 | 6 | 82% |
| `sdd/nucleo/` | 57 | 5 | 5 | 89% |
| `sdd/nucleo/cadastro-de-usuario/` | 56 | 3 | 5 | 90% |
| `sdd/nucleo/questoes-e-casos-de-teste/` | 46 | 4 | 6 | 86% |
| `sdd/nucleo/ranking-e-conquistas/` | 40 | 3 | 7 | 83% |
| `sdd/nucleo/submissao-e-avaliacao-de-codigo/` | 48 | 3 | 5 | 88% |
| `sdd/projetos/` | 39 | 5 | 3 | 88% |
| `sdd/projetos/ciclo-de-vida-do-projeto/` | 40 | 5 | 3 | 89% |

## Perguntas de Validação

Foram geradas e respondidas **7 perguntas** em [`sdd/questions.md`](questions.md). Não há respostas pendentes.

## Lacunas que permanecem

- 🔴 Política operacional de retry/estado terminal da fila RQ quando o worker falha antes de persistir resultado.
- 🔴 Constraint contra participações duplicadas na mesma avaliação, inclusive em criação concorrente.
- 🔴 Semântica de sessões simultâneas e confiança/proxy para `X-Forwarded-For` no registro de atividade.
- 🔴 Recuperação das associações de containers e WebSockets após reinício do serviço Node; os Maps atuais são voláteis.
- 🔴 TTL e invalidação do cache do ranking não estão definidos no fluxo observado.
- 🔴 Confirmação de e-mail, rate limiting de autenticação e configuração operacional de SMTP não foram encontrados.
- 🔴 Segurança de execução em produção depende da configuração efetiva do Docker Engine e do host.
- 🔴 O comportamento atual do worker diverge da decisão confirmada: sem casos de teste deixa `Waiting`, mas o contrato alvo deve terminar em `OK`.

## Recomendações

- [ ] Implementar as sete decisões confirmadas pelo usuário, mantendo os desvios do legado explícitos até que o código seja atualizado.
- [ ] Priorizar autorização por proprietário em submissões, avaliações, arquivos do editor e WebSockets.
- [ ] Definir política operacional de retry e recuperação de ambientes antes de reimplementar workers/IDE.
- [ ] Validar proxy e tratamento de IP antes de usar métricas de atividade para auditoria.

## Histórico de Reclassificações

| De | Para | Afirmação | Evidência |
|----|------|-----------|-----------|
| 🔴 | 🟢 | Questão sem casos termina aprovada (`OK`). | Resposta do usuário em `sdd/questions.md`, Pergunta 1; divergência legada em `core/worker.py:5`. |
| 🔴 | 🟢 | Início/consulta de avaliação só ocorre dentro da janela ativa. | Resposta do usuário, Pergunta 2; `Assessment.is_available` em `evaluation/models.py:39`. |
| 🔴 | 🟢 | Participação de avaliação é privada ao aluno e staff autorizado. | Resposta do usuário, Pergunta 3. |
| 🔴 | 🟢 | Status de submissão é privado ao autor e staff autorizado. | Resposta do usuário, Pergunta 4; lacuna atual em `core/views.py:310`. |
| 🔴 | 🟢 | Arquivos e resultados Runner são privados ao owner e staff autorizado. | Resposta do usuário, Pergunta 5. |
| 🔴 | 🟢 | WebSocket valida sessão/proprietário em cada operação e confina caminhos ao workspace. | Resposta do usuário, Pergunta 6. |
| 🔴 | 🟢 | Excluir projeto remove container e workspace. | Resposta do usuário, Pergunta 7; view legada em `projects/views.py:82`. |

## Revisão Cruzada

Não realizada: nível Essencial não oferece revisão cruzada externa.
