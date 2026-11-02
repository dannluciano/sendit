# Domínio do SendIT

## Glossário

| Termo | Significado no código |
|---|---|
| Questão | Desafio de programação com enunciado, tags, XP, visibilidade e casos de teste. |
| Caso de teste | Par entrada/saída esperada associado a uma questão. |
| Submissão | Código enviado por um usuário para uma questão; avaliado de forma assíncrona. |
| Runner | Execução avulsa do editor, sem associação necessária a uma questão. |
| Avaliação | Conjunto de questões com pontos e janela temporal, relacionado a grupos/turmas. |
| Participação | Registro de um aluno em uma avaliação, com pontuação computada pelas submissões corretas no período. |
| Projeto | Workspace nomeado e pertencente a um usuário, aberto em ambiente de IDE isolado. |
| Conquista | Badge associado a usuários e XP; pode ser oculto. |
| LogRecord | Período de atividade associado ao username, com check-in, check-out e IP. |

## Regras confirmadas

1. Questões invisíveis não aparecem na lista normal nem na seleção aleatória de questões pendentes.
2. Uma questão resolvida é aquela que tem submissão com status `OK` para o usuário.
3. O sistema não cria outra submissão para a mesma questão após solução correta; também bloqueia novas tentativas em janela de 15 segundos.
4. Submissões são avaliadas por worker RQ. Os casos de teste são executados até o primeiro que falha; o status/saída/log desse caso são persistidos.
5. O executor valida/compila e roda o código em container Docker com limites explícitos de recurso, sem rede e com filesystem somente leitura.
6. A saída é comparada por linhas com a saída esperada; a comparação não roda se a saída esperada estiver vazia.
7. XP de ranking soma XP das questões resolvidas e XP das conquistas. O nível usa `min(int(sqrt(XP de questões) * 1.5), 74)` (a implementação SQL aplica `LEAST`).
8. O ranking exclui grupo `Staff`; pode ser filtrado por grupo. As avaliações exibidas ao usuário dependem do grupo do usuário e da janela temporal.
9. A pontuação de avaliação soma os pontos de cada questão com submissão correta dentro da janela estrita da avaliação.
10. Projetos têm nomes únicos por proprietário e caracteres permitidos limitados a letras ASCII, números, `_` e `-`.
11. Os arquivos da IDE são atualizados pela chave `(owner, name)`.
12. O nível de acesso à IDE é aplicado por cookie assinado nas rotas HTTP `/api/*`; o processo Node mantém os ambientes em memória.

## Evidências históricas (Git)

- 🟢 O commit `4bfb1bd1` substituiu a execução local/subprocessos por execução em Docker, incluindo seleção de imagens por linguagem, timeout e limites de CPU/memória. A mudança indica decisão de isolar execução de código enviado por usuários.
- 🟢 Os commits `f25a39e5` e `803ab3c7` corrigiram montagem e diretório temporário da IDE em produção, confirmando que o workspace precisa ser compartilhado corretamente entre host e container.
- 🟢 `8a241c1d` e `24c71750` tratam da paginação do ranking, evidenciando volume de resultados como preocupação funcional.
- 🟡 Estas interpretações são inferidas dos títulos e diffs selecionados; não há ADRs originais encontrados nesta leitura.

## Lacunas de domínio

- 🔴 Regras de penalidade, tentativas máximas ou nota parcial não foram identificadas; o worker atual interrompe no primeiro caso falho.
- 🔴 O legado não verifica janela em `assessment_start`; o usuário confirmou que o contrato alvo deve negar início/consulta fora do período.
- 🟢 O usuário confirmou validação da sessão Django e propriedade do projeto em WebSocket; integração concreta no deploy ainda requer implementação.
- 🟢 O usuário confirmou `OK` para questão sem casos; o legado atualmente deixa `Waiting`.

## Confiança

Regras descritas como confirmadas foram observadas no código. Intenções históricas são inferidas de commits; lacunas devem ser validadas por responsáveis do produto.

## Regras de produto confirmadas na revisão

- Submissão de questão sem casos de teste deve ser aprovada (`OK`); o worker legado atualmente deixa `Waiting`. 🟢 Confirmado pelo usuário em 2026-11-02.
- Início e consulta de avaliação devem ocorrer somente dentro da janela; participação é privada ao aluno e staff autorizado. 🟢 Confirmado pelo usuário em 2026-11-02.
- Status de submissão é privado ao autor e staff autorizado. 🟢 Confirmado pelo usuário em 2026-11-02.
- Arquivos e resultados de Runner são privados ao owner e staff autorizado. 🟢 Confirmado pelo usuário em 2026-11-02.
- WebSocket da IDE valida sessão Django e propriedade do projeto em cada operação; filesystem é confinado ao workspace. 🟢 Confirmado pelo usuário em 2026-11-02.
- Excluir projeto remove container e diretório workspace. 🟢 Confirmado pelo usuário em 2026-11-02.

Essas regras definem o contrato alvo; onde indicado, o legado atual diverge.
