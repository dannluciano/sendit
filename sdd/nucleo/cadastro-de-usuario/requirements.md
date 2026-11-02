# Cadastro e autenticação, Requirements

## Visão Geral

Esta unit cobre criação de conta, login/logout Django e rotas de recuperação de senha. No cadastro, o usuário informa username, nome, sobrenome, e-mail e duas entradas de senha; ao criar conta com sucesso, a sessão é aberta automaticamente. 🟢

## Responsabilidades

- Validar e criar usuário usando `UserCreationForm` do Django. 🟢
- Impedir cadastro pela tela quando o usuário já está autenticado. 🟢
- Autenticar, encerrar e recuperar acesso por rotas Django. 🟢

## Regras de Negócio

- Nome, sobrenome e e-mail são obrigatórios no formulário de cadastro; username e senhas são providos pela classe base do Django. 🟢
- O e-mail do modelo de usuário é marcado como único durante a importação de `core.models`. 🟢
- Cadastro válido autentica o novo usuário e redireciona para `/home/`. 🟢
- Usuário autenticado que abre `/signup/` é redirecionado para home. 🟢
- 🔴 Política de verificação de e-mail, confirmação de identidade e política de username precisa ser validada; não aparece implementada no fluxo observado.

## Requisitos Funcionais

| ID | Requisito | Prioridade | Critério de Aceite |
|----|-----------|-----------|-------------------|
| RF-01 | Exibir formulário de cadastro com username, nome, sobrenome, e-mail e confirmação de senha. 🟢 | Must | GET `/signup/` renderiza formulário com campos e labels esperados. |
| RF-02 | Validar os dados e persistir usuário quando o formulário for válido. 🟢 | Must | POST válido cria exatamente um usuário e inicia sessão autenticada. |
| RF-03 | Reexibir formulário com erros quando o cadastro for inválido. 🟢 | Must | POST inválido não cria usuário e retorna formulário com erros associados. |
| RF-04 | Usar login/logout e recuperação de senha providos pelo Django. 🟢 | Should | Rotas configuradas aceitam o fluxo padrão Django e redirecionamentos definidos. |

## Requisitos Não Funcionais

| Tipo | Requisito inferido | Evidência no código | Confiança |
|------|--------------------|---------------------|-----------|
| Segurança | Senha deve respeitar validadores configurados pelo Django e a sessão é aberta com autenticação Django. | `SendIT/settings.py:113`, `core/views.py:31` | 🟢 |
| Segurança | E-mail único evita mais de uma conta com o mesmo e-mail, sujeito à persistência da constraint correspondente. | `core/models.py:15` | 🟢 |

## Critérios de Aceitação

```gherkin
# 🟢 Happy path
Dado um visitante com dados de cadastro válidos
Quando ele envia o formulário de cadastro
Então uma conta é criada, a sessão é autenticada e ele é redirecionado para home

# 🟢 Erro de validação
Dado um visitante que envia campos inválidos ou senhas incompatíveis
Quando o formulário é submetido
Então o sistema não cria a conta e reapresenta o formulário com erros

# 🟢 Usuário existente
Dado um usuário já autenticado
Quando ele abre a página de cadastro
Então o sistema o redireciona para home
```

## Prioridade (MoSCoW)

| Requisito | MoSCoW | Justificativa |
|-----------|--------|---------------|
| Criar e autenticar conta | Must | Necessário para acessar áreas protegidas. 🟢 |
| Login e logout | Must | Base da sessão usada pelos módulos do produto. 🟢 |
| Recuperação de senha | Should | Rota disponível pelo Django, mas não compõe o caminho de primeiro acesso. 🟢 |
| Verificação de e-mail | Won't | Não foi identificada implementação no legado analisado. 🟢 |

## Rastreabilidade de Código

| Arquivo | Função / Classe | Cobertura |
|---------|-----------------|-----------|
| `core/forms.py` | `SignUpForm` | 🟢 |
| `core/views.py` | `signup` | 🟢 |
| `core/urls.py` | Login, logout e signup | 🟢 |
| `SendIT/urls.py` | Password reset routes | 🟢 |
| `SendIT/settings.py` | Validadores e redirects de autenticação | 🟢 |
| `core/models.py` | Unicidade do e-mail | 🟢 |
