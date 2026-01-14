# 🔐 Guia de Configuração - CRECI Itinerante

## 📋 Índice
1. [Configuração do Google Sheets API](#1-configuração-do-google-sheets-api)
2. [Configuração das Credenciais](#2-configuração-das-credenciais)
3. [Preparação das Planilhas](#3-preparação-das-planilhas)
4. [Configuração da Autenticação](#4-configuração-da-autenticação)
5. [Primeiro Acesso](#5-primeiro-acesso)

---

## 1. Configuração do Google Sheets API

### Passo 1.1: Criar Projeto no Google Cloud Console

1. Acesse [Google Cloud Console](https://console.cloud.google.com/)
2. Clique em **"Select a project"** → **"NEW PROJECT"**
3. Nome do projeto: `CRECI-Itinerante`
4. Clique em **"CREATE"**

### Passo 1.2: Ativar APIs Necessárias

1. No menu lateral, vá em **"APIs & Services"** → **"Library"**
2. Procure e ative as seguintes APIs:
   - **Google Sheets API**
   - **Google Drive API**

### Passo 1.3: Criar Service Account

1. Vá em **"APIs & Services"** → **"Credentials"**
2. Clique em **"+ CREATE CREDENTIALS"** → **"Service account"**
3. Preencha:
   - **Service account name**: `creci-sheets-reader`
   - **Service account ID**: (gerado automaticamente)
   - **Description**: `Service account para ler planilhas do CRECI`
4. Clique em **"CREATE AND CONTINUE"**
5. Em **"Grant this service account access to project"**:
   - Role: **Editor** (ou **Viewer** se for apenas leitura)
6. Clique em **"DONE"**

### Passo 1.4: Gerar Chave JSON

1. Na lista de Service Accounts, clique na que você criou
2. Vá na aba **"KEYS"**
3. Clique em **"ADD KEY"** → **"Create new key"**
4. Selecione **"JSON"**
5. Clique em **"CREATE"**
6. Um arquivo JSON será baixado automaticamente
7. **Renomeie o arquivo para `google_credentials.json`**
8. **Mova o arquivo para a pasta raiz do projeto**

---

## 2. Configuração das Credenciais

### Passo 2.1: Criar Arquivo .env

1. Copie o arquivo `.env.example` e renomeie para `.env`:
   ```powershell
   Copy-Item .env.example .env
   ```

### Passo 2.2: Gerar Hash da Senha do Admin

Execute no terminal PowerShell:

```powershell
python -c "import bcrypt; senha='SUA_SENHA_AQUI'; print(bcrypt.hashpw(senha.encode(), bcrypt.gensalt()).decode())"
```

**Substitua `SUA_SENHA_AQUI` pela senha desejada.**

Copie o hash gerado (algo como: `$2b$12$abc123...`).

### Passo 2.3: Preencher o Arquivo .env

Abra o arquivo `.env` e preencha:

```env
# =====================================================================
# AUTENTICAÇÃO - Usuário Admin
# =====================================================================
ADMIN_USERNAME=admin
ADMIN_PASSWORD_HASH=$2b$12$SEU_HASH_AQUI
ADMIN_NAME=Seu Nome

# =====================================================================
# GOOGLE SHEETS - URLs das Planilhas
# =====================================================================
GOOGLE_SHEET_CORRETORES=https://docs.google.com/spreadsheets/d/SEU_ID_AQUI/edit
GOOGLE_SHEET_IMOBILIARIAS=https://docs.google.com/spreadsheets/d/SEU_ID_AQUI/edit

# =====================================================================
# GOOGLE SHEETS - Credenciais da Service Account
# =====================================================================
GOOGLE_CREDENTIALS_FILE=google_credentials.json

# =====================================================================
# CONFIGURAÇÕES OPCIONAIS
# =====================================================================
SHEET_NAME_CORRETORES=Corretores
SHEET_NAME_IMOBILIARIAS=Imobiliárias
SHEETS_TIMEOUT=30
```

---

## 3. Preparação das Planilhas

### Passo 3.1: Criar/Mover Planilhas para Google Sheets

1. Acesse [Google Sheets](https://sheets.google.com/)
2. Crie ou faça upload das planilhas de **Corretores** e **Imobiliárias**
3. Certifique-se que cada planilha tenha as seguintes colunas:
   - **CIDADE** (nome da cidade)
   - **UF** (deve ser "BA" ou "Bahia")
   - **QUANTIDADE** (total de corretores/imobiliárias)
   - **REGULAR** (quantidade regular)
   - **IRREGULAR** (quantidade irregular)

### Passo 3.2: Compartilhar Planilhas com a Service Account

1. Abra o arquivo `google_credentials.json`
2. Copie o valor do campo `"client_email"` (algo como: `creci-sheets-reader@...iam.gserviceaccount.com`)
3. Em cada planilha do Google Sheets:
   - Clique em **"Share"** (botão verde no canto superior direito)
   - Cole o email da service account
   - Permissão: **Viewer** (apenas leitura)
   - **DESMARQUE** a opção "Notify people"
   - Clique em **"Share"**

### Passo 3.3: Copiar URLs das Planilhas

1. Abra cada planilha no navegador
2. Copie a URL completa (exemplo: `https://docs.google.com/spreadsheets/d/1abc...xyz/edit`)
3. Cole no arquivo `.env` nas variáveis correspondentes

---

## 4. Configuração da Autenticação

### Estrutura de Segurança

O sistema usa:
- **bcrypt** para hash de senhas
- **Sessões do Streamlit** para manter login
- **Variáveis de ambiente** para credenciais sensíveis

### Adicionar Mais Usuários (Futuro)

Para adicionar mais usuários, você pode:
1. Criar um banco de dados SQLite
2. Ou adicionar mais variáveis no `.env` (`USER2_USERNAME`, etc.)

---

## 5. Primeiro Acesso

### Passo 5.1: Instalar Dependências

```powershell
# Ativar ambiente virtual
.\.venv\Scripts\Activate.ps1

# Instalar pacotes
pip install -r requirements.txt
```

### Passo 5.2: Executar o Sistema

```powershell
streamlit run app.py
```

### Passo 5.3: Fazer Login

1. O sistema abrirá no navegador
2. Digite as credenciais configuradas no `.env`:
   - **Usuário**: valor de `ADMIN_USERNAME`
   - **Senha**: a senha que você usou para gerar o hash (NÃO o hash)
3. Clique em **"Entrar"**

---

## 🔒 Segurança - Checklist

- [ ] Arquivo `.env` **NÃO** está no Git (verificar `.gitignore`)
- [ ] Arquivo `google_credentials.json` **NÃO** está no Git
- [ ] Arquivos `.xlsx` **NÃO** estão no Git
- [ ] Service Account tem apenas permissões de **Viewer** nas planilhas
- [ ] Senha do admin é forte (mínimo 8 caracteres, letras, números, símbolos)
- [ ] Planilhas do Google Sheets **NÃO** estão públicas (apenas compartilhadas com a Service Account)

---

## 🛠️ Solução de Problemas

### Erro: "Arquivo de credenciais não encontrado"
- Verifique se `google_credentials.json` está na pasta raiz do projeto
- Verifique o nome do arquivo no `.env` (`GOOGLE_CREDENTIALS_FILE`)

### Erro: "Permission denied" no Google Sheets
- Certifique-se que compartilhou a planilha com o email da Service Account
- Verifique se o email copiado está correto

### Erro: "Usuário ou senha inválidos"
- Verifique se o hash da senha está correto no `.env`
- Certifique-se que está usando a senha original, não o hash

### Erro: "No module named 'gspread'"
- Execute: `pip install -r requirements.txt`

### Dados não aparecem no mapa
- Verifique se as colunas das planilhas estão corretas
- Verifique se existe coluna "UF" com valor "BA"
- Veja os logs no sidebar para mensagens de erro

---

## 📞 Suporte

Para problemas técnicos, consulte a documentação oficial:
- [Google Sheets API](https://developers.google.com/sheets/api)
- [Streamlit](https://docs.streamlit.io/)
- [gspread](https://docs.gspread.org/)

---

**Sistema desenvolvido com segurança e boas práticas! 🔐**
