# Cadastro e autenticação, Design Técnico

## Interface

| Símbolo | Assinatura | Retorno | Observação |
|---------|-----------|---------|------------|
| `SignUpForm` | `UserCreationForm(request.POST)` | formulário validado ou erros | Campos: username, first_name, last_name, email, password1, password2. |
| `signup` | `(request)` | render ou redirect | GET mostra formulário; POST valida/cria e autentica. |
| `LoginView` | Django class-based view | sessão Django | Template `platform/login.html`; redireciona usuário já autenticado. |
| `LogoutView` | Django class-based view | redirect `/` | Finaliza sessão. |
| Password reset views | Django class-based views | páginas/redirects Django | URLs em `SendIT/urls.py`. |

| Método | Caminho | Entrada | Saída | Status codes |
|--------|---------|---------|-------|--------------|
| GET/POST | `/` | credenciais no POST | login/redirect | Django defaults 🟢 |
| GET | `/logout/` | sessão | redirect `/` | Django defaults 🟢 |
| GET/POST | `/signup/` | username, nome, sobrenome, email e senha | formulário ou redirect `/home/` | render/redirect 🟢 |
| GET/POST | `/password_reset/` | e-mail | fluxo Django de reset | Django defaults 🟢 |
| GET | `/password_reset/done/` | — | confirmação | Django defaults 🟢 |
| GET/POST | `/reset/<uidb64>/<token>/` | token e nova senha | confirmação de reset | Django defaults 🟢 |
| GET | `/reset/done/` | — | confirmação final | Django defaults 🟢 |

## Fluxo Principal

1. `GET /signup/` instancia `SignUpForm` com username, nome, sobrenome e e-mail vazios e renderiza `platform/signup.html`. 🟢
2. `POST /signup/` valida `SignUpForm`, herdado de `UserCreationForm`; regras e validação de senha vêm do Django. 🟢
3. Em sucesso, `form.save()` cria usuário, `authenticate(username, raw_password)` autentica e `login()` cria a sessão. 🟢
4. A view redireciona para `core:home`. 🟢
5. Em erro de validação, renderiza novamente o template com o formulário e seus erros. 🟢

## Fluxos Alternativos

- **Conta já autenticada abre signup:** redireciona para home antes de processar formulário. 🟢
- **Login:** usa `LoginView` padrão de Django com `redirect_authenticated_user=True`. 🟢
- **Logout:** usa `LogoutView` padrão e redireciona para raiz. 🟢
- **Recuperação de senha:** views padrão Django recebem e-mail, token e nova senha. 🟢
- 🔴 Não há fluxo de confirmação de e-mail ou de moderação antes do login automático.

## Dependências

- `django.contrib.auth`: modelos, formulários, autenticação, sessão e recuperação de senha.
- `core.models.User`: modelo padrão de usuário, com e-mail marcado como único.
- `platform/signup.html` e `platform/login.html`: renderização dos formulários.
- `SendIT/settings.py`: validadores de senha, `LOGIN_URL`, redirects e backend de e-mail SMTP.

## Decisões de Design Identificadas

| Decisão | Evidência no código | Confiança |
|---------|---------------------|-----------|
| Reutilizar `UserCreationForm` para criação de conta | `core/forms.py:8` | 🟢 |
| Abrir sessão imediatamente após cadastro válido | `core/views.py:36` | 🟢 |
| Delegar login/logout/reset às views padrão do Django | `core/urls.py:8`, `SendIT/urls.py:27` | 🟢 |
| Exigir e-mail único no modelo | `core/models.py:15` | 🟢 |

## Estado Interno

O cadastro não mantém estado próprio: usuário é persistido no modelo Django e autenticação vive na sessão padrão. Tokens de recuperação são geridos pelo fluxo Django. 🟢

## Observabilidade

Não foram identificados logs de negócio específicos para cadastro/login nesta unit. 🟢

## Riscos e Lacunas

- 🔴 Configuração de envio SMTP e conteúdo dos e-mails não foi explorada nesta unit.
- 🔴 Política de privacidade, confirmação de e-mail e rate limiting de autenticação não foram identificados.
- 🟡 O campo e-mail é marcado único por alteração em runtime de `_meta`; verificar geração da constraint em migrations da instalação final.
