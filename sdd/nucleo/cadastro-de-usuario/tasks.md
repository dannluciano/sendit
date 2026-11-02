# Cadastro e autenticação, Tarefas de Implementação

## Pré-requisitos

- [ ] Django auth e templates de login/cadastro configurados.
- [ ] Backend de e-mail configurado para recuperação de senha.
- [ ] Schema de usuário e unicidade de e-mail aplicados.

## Tarefas

- [ ] T-01, Criar formulário de cadastro baseado em `UserCreationForm` com campos de perfil obrigatórios.
  - Origem no legado: `core/forms.py:8`
  - Critério de pronto: nome, sobrenome, e-mail, username e senhas são validados; senha segue validadores configurados.
  - Confiança: 🟢

- [ ] T-02, Implementar cadastro com autenticação automática e redirect para home.
  - Origem no legado: `core/views.py:31`
  - Critério de pronto: POST válido salva usuário, inicia sessão e redireciona; POST inválido reexibe erros.
  - Confiança: 🟢

- [ ] T-03, Implementar login e logout com views padrão Django e redirects configurados.
  - Origem no legado: `core/urls.py:8`, `SendIT/settings.py:229`
  - Critério de pronto: login cria sessão e logout a encerra conforme caminhos atuais.
  - Confiança: 🟢

- [ ] T-04, Expor fluxo padrão Django de recuperação e redefinição de senha.
  - Origem no legado: `SendIT/urls.py:27`
  - Critério de pronto: usuário recebe e-mail de reset e token válido permite definir nova senha.
  - Confiança: 🟢

- [ ] T-05, Garantir unicidade do e-mail da conta.
  - Origem no legado: `core/models.py:15`
  - Critério de pronto: tentativa de persistir e-mail já associado é rejeitada de forma compreensível.
  - Confiança: 🟢

## Tarefas de Teste

- [ ] TT-01, Testar cadastro válido, erros de campo, senha inválida e senha divergente.
  - Origem no legado: `core/forms.py:8`, `core/views.py:31`
  - Critério de pronto: conta só é criada com dados válidos; erros são apresentados sem sessão autenticada.
  - Confiança: 🟢
- [ ] TT-02, Testar redirecionamento de usuário autenticado para fora da tela de cadastro.
  - Origem no legado: `core/views.py:32`
  - Critério de pronto: usuário autenticado não vê nem reenvia formulário de criação.
  - Confiança: 🟢
- [ ] TT-03, Testar ciclo de login/logout e redefinição por token.
  - Origem no legado: `core/urls.py:8`, `SendIT/urls.py:27`
  - Critério de pronto: sessão é estabelecida/encerrada e token inválido não altera senha.
  - Confiança: 🟡 comportamento de token é fornecido pelo Django.

## Tarefas de Migração de Dados

- [ ] TM-01, Verificar constraint de unicidade do e-mail no schema aplicado.
  - Origem no legado: `core/models.py:15`, `core/migrations/`
  - Critério de pronto: banco rejeita duplicidade, não apenas o formulário.
  - Confiança: 🟡 a alteração `_meta` em runtime exige confirmação do schema gerado/aplicado.

## Ordem Sugerida

1. Confirmar o modelo/schema e restrição do e-mail.
2. Implementar formulário e view de cadastro.
3. Ligar login, logout e password reset às configurações de e-mail.
4. Cobrir a jornada de conta com testes de integração.

## Lacunas Pendentes (🔴)

- Definir se cadastro requer confirmação de e-mail antes de liberar a sessão.
- Validar limites/rate limiting para tentativas de login, cadastro e solicitação de reset.
- Confirmar conteúdo e origem do e-mail de recuperação em cada ambiente.
