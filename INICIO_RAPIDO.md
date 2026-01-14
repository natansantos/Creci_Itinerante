# 🚀 Guia Rápido de Execução - CRECI Itinerante

## ⚡ Início Rápido (Primeira Vez)

### 1️⃣ Instalar Dependências

```powershell
# Ativar ambiente virtual
.\.venv\Scripts\Activate.ps1

# Instalar pacotes
pip install -r requirements.txt
```

### 2️⃣ Configurar Credenciais

#### A. Gerar Hash da Senha
```powershell
python gerar_senha.py
```
Digite sua senha e copie o hash gerado.

#### B. Criar Arquivo .env
```powershell
# Copiar template
Copy-Item .env.example .env

# Editar o arquivo .env e preencher:
# - ADMIN_PASSWORD_HASH (cole o hash gerado)
# - URLs das planilhas do Google Sheets
```

#### C. Configurar Google Sheets
Siga o guia detalhado em [GUIA_CONFIGURACAO.md](GUIA_CONFIGURACAO.md), seção 1 e 3.

### 3️⃣ Executar o Sistema

```powershell
streamlit run app.py
```

O sistema abrirá automaticamente no navegador.

---

## 🔄 Execução Subsequente (Uso Diário)

```powershell
# 1. Ativar ambiente virtual
.\.venv\Scripts\Activate.ps1

# 2. Executar
streamlit run app.py
```

---

## 📋 Checklist Pré-Execução

Antes de executar pela primeira vez, certifique-se:

- [ ] Ambiente virtual criado e ativado
- [ ] Dependências instaladas (`pip install -r requirements.txt`)
- [ ] Arquivo `.env` criado e preenchido
- [ ] Arquivo `google_credentials.json` na pasta raiz
- [ ] Planilhas do Google Sheets compartilhadas com a Service Account
- [ ] Hash da senha gerado e adicionado ao `.env`

---

## 🔐 Fazendo Login

1. Abra o sistema no navegador (geralmente `http://localhost:8501`)
2. Digite:
   - **Usuário**: valor de `ADMIN_USERNAME` no `.env` (padrão: `admin`)
   - **Senha**: a senha original que você usou para gerar o hash
3. Clique em **"Entrar"**

---

## ❌ Problemas Comuns

### "Module not found"
```powershell
pip install -r requirements.txt
```

### "Arquivo de credenciais não encontrado"
Verifique se `google_credentials.json` está na pasta raiz do projeto.

### "Permission denied" do Google Sheets
Compartilhe as planilhas com o email da Service Account (veja [GUIA_CONFIGURACAO.md](GUIA_CONFIGURACAO.md)).

### "Usuário ou senha inválidos"
- Verifique se o hash no `.env` está correto
- Use a senha ORIGINAL, não o hash

---

## 📚 Documentação Completa

- **Configuração inicial**: [GUIA_CONFIGURACAO.md](GUIA_CONFIGURACAO.md)
- **Sobre o sistema**: [README.md](README.md)

---

## 🎯 Comandos Úteis

```powershell
# Gerar novo hash de senha
python gerar_senha.py

# Atualizar dependências
pip install -r requirements.txt --upgrade

# Ver versão do Python
python --version

# Listar pacotes instalados
pip list
```

---

**Pronto para começar! 🚀**
