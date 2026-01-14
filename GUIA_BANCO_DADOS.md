# 🗄️ Guia do Banco de Dados de Usuários

## 📋 Visão Geral

O sistema usa banco de dados para gerenciar usuários, permitindo:
- ✅ Criar múltiplos usuários
- ✅ Definir diferentes papéis (admin/user)
- ✅ Ativar/desativar usuários
- ✅ Alterar senhas
- ✅ Funciona local (SQLite) e cloud (PostgreSQL)

---

## 🏗️ Arquitetura

### Desenvolvimento Local
- **SQLite** (`data/users.db`)
- Arquivo criado automaticamente
- Não versionado no Git

### Produção (Streamlit Cloud)
- **PostgreSQL** (Railway, Supabase, Heroku, etc.)
- Credenciais em `st.secrets`

---

## 🚀 Configuração Local

### 1. Nenhuma configuração necessária!

O sistema cria automaticamente:
- Pasta `data/`
- Arquivo `users.db`
- Usuário admin a partir do `.env`

### 2. Primeiro Acesso

Execute o app normalmente:
```powershell
streamlit run app.py
```

O admin do `.env` será criado automaticamente no banco.

---

## ☁️ Configuração no Streamlit Cloud

### 1. Criar Banco PostgreSQL

Opções gratuitas:
- **Railway**: [railway.app](https://railway.app)
- **Supabase**: [supabase.com](https://supabase.com)
- **ElephantSQL**: [elephantsql.com](https://elephantsql.com)
- **Neon**: [neon.tech](https://neon.tech)

### 2. Obter URL de Conexão

Após criar o banco, copie a `DATABASE_URL`:
```
postgresql://usuario:senha@host:5432/database
```

### 3. Adicionar aos Secrets do Streamlit

No Streamlit Cloud, em **Settings → Secrets**:

```toml
# ... outras configurações ...

# =====================================================================
# BANCO DE DADOS
# =====================================================================
DATABASE_URL = "postgresql://usuario:senha@host:5432/database"
```

### 4. Deploy

O sistema detectará automaticamente a `DATABASE_URL` e usará PostgreSQL.

---

## 👥 Gerenciamento de Usuários

### Interface Admin

Apenas usuários com role `admin` têm acesso ao menu **"Gerenciar Usuários"**.

#### Funcionalidades:

1. **Listar Usuários**
   - Ver todos os usuários
   - Status (ativo/inativo)
   - Papel (admin/user)
   - Editar inline

2. **Adicionar Usuário**
   - Username único
   - Senha mínima de 6 caracteres
   - Nome completo
   - Definir papel

3. **Alterar Senha**
   - Trocar senha de qualquer usuário
   - Admin pode resetar senhas

---

## 🔒 Papéis de Usuário

### Admin
- ✅ Acesso ao mapa e dados
- ✅ Gerenciar usuários
- ✅ Criar/editar/desativar usuários
- ✅ Alterar senhas

### User
- ✅ Acesso ao mapa e dados
- ❌ Sem acesso a gerenciamento

---

## 📊 Estrutura do Banco

### Tabela: `users`

| Campo | Tipo | Descrição |
|-------|------|-----------|
| id | INTEGER/SERIAL | ID único (PK) |
| username | TEXT/VARCHAR(50) | Nome de usuário (único) |
| password_hash | TEXT/VARCHAR(255) | Hash bcrypt da senha |
| full_name | TEXT/VARCHAR(100) | Nome completo |
| role | TEXT/VARCHAR(20) | admin ou user |
| active | BOOLEAN | Ativo ou inativo |
| created_at | TIMESTAMP | Data de criação |

---

## 🛠️ Uso Programático

### Criar Usuário

```python
from user_database import get_user_database

db = get_user_database()
db.create_user(
    username="joao",
    password="senha123",
    full_name="João Silva",
    role="user"
)
```

### Buscar Usuário

```python
user = db.get_user("joao")
if user:
    print(f"Nome: {user['full_name']}")
    print(f"Papel: {user['role']}")
```

### Listar Todos

```python
users = db.list_users()
for user in users:
    print(f"{user['username']} - {user['full_name']}")
```

### Alterar Senha

```python
db.change_password("joao", "nova_senha_123")
```

### Desativar Usuário

```python
db.update_user("joao", active=False)
```

---

## 🔄 Migração do Sistema Antigo

Se você está migrando do sistema com credenciais apenas no `.env`:

### Opção 1: Manter Modo Legado

No [app.py](app.py), altere:
```python
authenticator = Authenticator(use_database=False)
```

### Opção 2: Migrar para Banco

1. O admin do `.env` é criado automaticamente no banco
2. Crie outros usuários pela interface
3. Continue usando normalmente

---

## 🧪 Testando Localmente

### 1. Criar Usuário de Teste

```powershell
streamlit run app.py
```

- Faça login como admin
- Vá em "Gerenciar Usuários"
- Adicione um novo usuário

### 2. Ver Banco SQLite

```powershell
# Instalar sqlite-browser ou usar CLI
sqlite3 data/users.db
```

```sql
SELECT * FROM users;
```

---

## 🔐 Segurança

### Checklist

- ✅ Senhas hasheadas com bcrypt
- ✅ Banco de dados local não versionado (`.gitignore`)
- ✅ Credenciais PostgreSQL em secrets (cloud)
- ✅ Validação de campos (username único, senha mínima)
- ✅ Soft delete (usuários desativados, não deletados)
- ✅ Admin não pode desativar a si mesmo

---

## 🛠️ Solução de Problemas

### Erro: "No module named 'psycopg2'"
```powershell
pip install psycopg2-binary
```

### Erro: "Database locked" (SQLite)
- Feche outras instâncias do app
- Ou adicione timeout: `conn = sqlite3.connect(db, timeout=10)`

### Banco não é criado
- Verifique permissões da pasta `data/`
- Veja logs do terminal

### Admin não consegue acessar gerenciamento
- Verifique se `user['role'] == 'admin'`
- Confira banco: `SELECT role FROM users WHERE username='admin'`

---

## 📝 Exemplos de Uso

### Criar Múltiplos Usuários via Script

```python
from user_database import get_user_database

db = get_user_database()

usuarios = [
    ("maria", "senha123", "Maria Santos", "user"),
    ("jose", "senha456", "José Oliveira", "user"),
    ("ana", "senha789", "Ana Costa", "admin"),
]

for username, password, name, role in usuarios:
    if not db.get_user(username):
        db.create_user(username, password, name, role)
        print(f"✅ {username} criado!")
```

---

**Sistema robusto de gerenciamento de usuários implementado! 👥**
