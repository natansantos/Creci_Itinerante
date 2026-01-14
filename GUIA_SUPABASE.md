# 🚀 Guia Completo: Supabase para CRECI Itinerante

## 📋 O que é Supabase?

Supabase é uma alternativa open source ao Firebase que oferece:
- ✅ PostgreSQL gerenciado (banco de dados gratuito)
- ✅ 500 MB de armazenamento gratuito
- ✅ Interface web amigável
- ✅ APIs automáticas
- ✅ Ideal para Streamlit Cloud

---

## 🎯 Passo 1: Criar Conta no Supabase

### 1.1. Acessar o Site
1. Vá em [https://supabase.com](https://supabase.com)
2. Clique em **"Start your project"**
3. Faça login com:
   - GitHub (recomendado)
   - Google
   - Email

### 1.2. Criar Nova Organização (se necessário)
1. Nome da organização: `CRECI` ou seu nome
2. Clique em **"Create organization"**

---

## 🗄️ Passo 2: Criar Projeto (Banco de Dados)

### 2.1. Criar Novo Projeto
1. No dashboard, clique em **"New project"**
2. Preencha:
   - **Name**: `creci-itinerante`
   - **Database Password**: Crie uma senha forte e **GUARDE** (você vai precisar)
   - **Region**: `South America (São Paulo)` (mais próximo do Brasil)
   - **Pricing Plan**: `Free` (gratuito)
3. Clique em **"Create new project"**
4. Aguarde 2-3 minutos (criação do banco)

### 2.2. Aguardar Provisionamento
- Status aparecerá como "Setting up project..."
- Quando ficar "Active", está pronto! ✅

---

## 🔗 Passo 3: Obter Credenciais de Conexão

### 3.1. Acessar Configurações
1. No menu lateral, clique em **⚙️ Project Settings**
2. Vá em **Database** (menu lateral)

### 3.2. Copiar Connection String
1. Role até a seção **"Connection string"**
2. Selecione a aba **"URI"**
3. Copie a string que aparece:
   ```
   postgresql://postgres.xxxxx:[YOUR-PASSWORD]@aws-0-sa-east-1.pooler.supabase.com:6543/postgres
   ```

### 3.3. Substituir a Senha
Na string copiada, substitua `[YOUR-PASSWORD]` pela senha que você criou no Passo 2.1.

**Exemplo:**
```
# String original:
postgresql://postgres.xxxxx:[YOUR-PASSWORD]@aws-0-sa-east-1.pooler.supabase.com:6543/postgres

# String com senha:
postgresql://postgres.xxxxx:MinhaSenh@123@aws-0-sa-east-1.pooler.supabase.com:6543/postgres
```

⚠️ **IMPORTANTE**: Guarde essa string completa em local seguro!

---

## 🧪 Passo 4: Testar Localmente

### 4.1. Adicionar ao .env Local

Abra o arquivo `.env` e adicione:

```env
# =====================================================================
# BANCO DE DADOS (Supabase)
# =====================================================================
DATABASE_URL=postgresql://postgres.xxxxx:SuaSenha@aws-0-sa-east-1.pooler.supabase.com:6543/postgres
```

### 4.2. Instalar Dependência PostgreSQL

```powershell
pip install psycopg2-binary
```

### 4.3. Testar a Aplicação

```powershell
streamlit run app.py
```

**O que deve acontecer:**
1. ✅ Sistema cria automaticamente a tabela `users`
2. ✅ Usuário admin é criado no banco
3. ✅ Você consegue fazer login
4. ✅ Menu "Gerenciar Usuários" aparece (se for admin)

---

## ☁️ Passo 5: Configurar no Streamlit Cloud

### 5.1. Acessar Secrets do App

1. Vá em [share.streamlit.io](https://share.streamlit.io)
2. Selecione seu app
3. Clique em **⚙️ Settings** → **Secrets**

### 5.2. Adicionar DATABASE_URL

No editor de secrets, adicione:

```toml
# =====================================================================
# BANCO DE DADOS (Supabase)
# =====================================================================
DATABASE_URL = "postgresql://postgres.xxxxx:SuaSenha@aws-0-sa-east-1.pooler.supabase.com:6543/postgres"

# ... resto das configurações ...
```

### 5.3. Salvar e Reiniciar

1. Clique em **"Save"**
2. O app reiniciará automaticamente
3. Aguarde 1-2 minutos

---

## 📊 Passo 6: Gerenciar Banco pelo Supabase

### 6.1. Ver Tabela de Usuários

1. No Supabase, vá em **🗄️ Table Editor** (menu lateral)
2. Você verá a tabela **`users`** criada automaticamente
3. Clique nela para ver os dados

### 6.2. Ver Dados da Tabela

Você verá colunas:
- `id` (auto-incremento)
- `username`
- `password_hash`
- `full_name`
- `role`
- `active`
- `created_at`

### 6.3. Editor SQL (Opcional)

1. Vá em **🔍 SQL Editor** (menu lateral)
2. Execute queries SQL:

```sql
-- Ver todos os usuários
SELECT id, username, full_name, role, active FROM users;

-- Contar usuários ativos
SELECT COUNT(*) FROM users WHERE active = true;

-- Ver apenas admins
SELECT * FROM users WHERE role = 'admin';
```

---

## 🔐 Passo 7: Adicionar Primeiro Usuário

### Método 1: Automático (Recomendado)

O sistema cria automaticamente o admin do `.env` na primeira execução.

### Método 2: Via Interface (após login como admin)

1. Faça login com o admin
2. Vá em **"Gerenciar Usuários"**
3. Tab **"Adicionar Usuário"**
4. Preencha e crie

### Método 3: Via SQL (avançado)

No Supabase SQL Editor:

```sql
INSERT INTO users (username, password_hash, full_name, role, active)
VALUES (
  'novousuario',
  '$2b$12$hash_gerado_aqui',  -- Use gerar_senha.py para gerar
  'Nome Completo',
  'user',
  true
);
```

---

## 📈 Passo 8: Monitoramento e Limites

### 8.1. Ver Uso do Banco

1. No Supabase, vá em **📊 Reports** (menu lateral)
2. Veja:
   - Database size
   - Number of tables
   - API requests

### 8.2. Limites do Plano Gratuito

- ✅ 500 MB de armazenamento
- ✅ 2 GB de transferência/mês
- ✅ 50.000 usuários autenticados/mês
- ✅ SSL incluído
- ✅ Backups semanais

**Para o CRECI Itinerante:**
- Tabela `users` ocupa ~1 KB por usuário
- Mesmo com 1000 usuários = ~1 MB
- Você está muito dentro do limite! ✅

---

## 🔄 Backup e Restauração

### Backup Manual

1. No Supabase, vá em **⚙️ Settings** → **Database**
2. Role até **"Database backups"**
3. Backups automáticos semanais (plano gratuito)
4. Clique em **"Download"** para backup manual

### Exportar Dados (SQL)

No SQL Editor:

```sql
-- Exportar todos os usuários
COPY (SELECT * FROM users) TO STDOUT WITH CSV HEADER;
```

---

## 🛠️ Solução de Problemas

### Erro: "Could not connect to server"

**Causa**: URL de conexão incorreta ou senha errada

**Solução**:
1. Verifique se copiou a URL completa
2. Confirme que substituiu `[YOUR-PASSWORD]` pela senha correta
3. Teste a conexão no Supabase SQL Editor

### Erro: "SSL connection required"

**Causa**: Supabase exige SSL

**Solução**: Adicione `?sslmode=require` ao final da URL:
```
postgresql://...postgres?sslmode=require
```

### Erro: "Permission denied"

**Causa**: Usuário postgres não tem permissão

**Solução**: Use a string de conexão fornecida pelo Supabase (não modifique)

### Tabela não é criada

**Causa**: Erro de conexão ou permissões

**Solução**:
1. Verifique logs do Streamlit
2. Teste conexão manualmente:

```python
import psycopg2
conn = psycopg2.connect("sua_connection_string")
print("✅ Conexão OK!")
```

### Senha com caracteres especiais

Se sua senha tem caracteres especiais (`@`, `#`, `%`, etc.), encode-os:
- `@` → `%40`
- `#` → `%23`
- `%` → `%25`
- `/` → `%2F`

**Exemplo:**
```
Senha: Senh@123#
URL: postgresql://postgres:Senh%40123%23@...
```

---

## 📊 Exemplo de Estrutura Final

### Arquivo .env (Local)
```env
# Admin
ADMIN_USERNAME=admin
ADMIN_PASSWORD_HASH=$2b$12$/UE9jxxnHz.dW86iF1/feeOefidtkIm7ghARwwbD1x4R4W.sIwiHW
ADMIN_NAME=Administrador CRECI

# Google Sheets
GOOGLE_SHEET_CORRETORES=https://docs.google.com/...
GOOGLE_SHEET_IMOBILIARIAS=https://docs.google.com/...

# Banco de Dados Supabase
DATABASE_URL=postgresql://postgres.xxx:senha@aws-0-sa-east-1.pooler.supabase.com:6543/postgres
```

### Streamlit Secrets (Cloud)
```toml
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD_HASH = "$2b$12$/UE9jxxnHz..."
ADMIN_NAME = "Administrador CRECI"

GOOGLE_SHEET_CORRETORES = "https://docs.google.com/..."
GOOGLE_SHEET_IMOBILIARIAS = "https://docs.google.com/..."

DATABASE_URL = "postgresql://postgres.xxx:senha@aws-0-sa-east-1.pooler.supabase.com:6543/postgres"

[gcp_service_account]
type = "service_account"
# ... resto das credenciais Google ...
```

---

## ✅ Checklist Final

Antes de fazer deploy, verifique:

- [ ] Projeto criado no Supabase
- [ ] DATABASE_URL copiada e senha substituída
- [ ] Testado localmente (`streamlit run app.py`)
- [ ] Tabela `users` criada automaticamente
- [ ] Admin consegue fazer login
- [ ] DATABASE_URL adicionada aos Secrets do Streamlit Cloud
- [ ] Deploy feito e app funcionando
- [ ] Consegue adicionar novos usuários pela interface

---

## 🎓 Recursos Adicionais

- **Documentação Supabase**: [https://supabase.com/docs](https://supabase.com/docs)
- **Dashboard Supabase**: [https://app.supabase.com](https://app.supabase.com)
- **Supabase Community**: [https://github.com/supabase/supabase/discussions](https://github.com/supabase/supabase/discussions)

---

**Banco de dados pronto para produção! 🎉**

Agora você tem:
- ✅ PostgreSQL gratuito e gerenciado
- ✅ Backup automático
- ✅ Interface visual para gerenciar dados
- ✅ Escalável até 500 MB
- ✅ Conectado ao Streamlit Cloud
