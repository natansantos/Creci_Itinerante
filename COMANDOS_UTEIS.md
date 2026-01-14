# ⚡ Comandos Úteis - CRECI Itinerante

## 🚀 Execução

### Iniciar o Sistema
```powershell
# Ativar ambiente virtual (se não estiver ativo)
.\.venv\Scripts\Activate.ps1

# Executar aplicação
streamlit run app.py
```

### Executar em uma Porta Específica
```powershell
streamlit run app.py --server.port 8502
```

### Executar sem Abrir o Navegador
```powershell
streamlit run app.py --server.headless true
```

---

## 🔐 Gerenciamento de Senha

### Gerar Hash de Nova Senha
```powershell
python gerar_senha.py
```

### Gerar Hash Passando Senha Como Argumento
```powershell
python gerar_senha.py "minha_senha_secreta"
```

### Gerar Hash Diretamente no Terminal
```powershell
python -c "import bcrypt; senha='SUA_SENHA'; print(bcrypt.hashpw(senha.encode(), bcrypt.gensalt()).decode())"
```

---

## 📦 Gerenciamento de Pacotes

### Instalar Todas as Dependências
```powershell
pip install -r requirements.txt
```

### Atualizar Todas as Dependências
```powershell
pip install -r requirements.txt --upgrade
```

### Instalar Pacote Específico
```powershell
pip install nome_do_pacote
```

### Listar Pacotes Instalados
```powershell
pip list
```

### Verificar Versão de Pacote Específico
```powershell
pip show streamlit
```

### Gerar requirements.txt Atualizado
```powershell
pip freeze > requirements_new.txt
```

---

## 🐍 Python

### Verificar Versão do Python
```powershell
python --version
```

### Executar Script Python
```powershell
python nome_script.py
```

### Verificar Caminho do Executável Python
```powershell
python -c "import sys; print(sys.executable)"
```

---

## 🗂️ Git

### Verificar Status (Arquivos Modificados)
```powershell
git status
```

### Adicionar Arquivos ao Stage
```powershell
git add .
```

### Fazer Commit
```powershell
git commit -m "Descrição das mudanças"
```

### Enviar para Repositório Remoto
```powershell
git push
```

### Ver Histórico de Commits
```powershell
git log --oneline
```

### Verificar Arquivos Ignorados pelo .gitignore
```powershell
git status --ignored
```

---

## 📊 Google Sheets

### Testar Conexão com Google Sheets (Python)
```powershell
python -c "from google_sheets import get_sheets_loader; loader = get_sheets_loader(); print('Autenticado!' if loader.authenticate() else 'Erro na autenticação')"
```

### Ver Email da Service Account
```powershell
python -c "import json; print(json.load(open('google_credentials.json'))['client_email'])"
```

---

## 🔍 Debugging

### Verificar Imports do Python
```powershell
python -c "import streamlit, pandas, folium, gspread, bcrypt; print('Todos os imports OK!')"
```

### Ver Variáveis de Ambiente do .env
```powershell
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('ADMIN_USERNAME:', os.getenv('ADMIN_USERNAME'))"
```

### Limpar Cache do Streamlit
```powershell
# Deletar pasta de cache
Remove-Item -Recurse -Force .streamlit
```

---

## 🧹 Limpeza

### Remover Cache Python
```powershell
# Remover __pycache__
Get-ChildItem -Recurse -Filter __pycache__ | Remove-Item -Recurse -Force

# Remover arquivos .pyc
Get-ChildItem -Recurse -Filter *.pyc | Remove-Item -Force
```

### Desativar Ambiente Virtual
```powershell
deactivate
```

---

## 📂 Arquivos

### Listar Estrutura do Projeto
```powershell
tree /F
```

### Copiar Arquivo
```powershell
Copy-Item arquivo_origem.txt arquivo_destino.txt
```

### Verificar se Arquivo Existe
```powershell
Test-Path arquivo.txt
```

### Ver Conteúdo de Arquivo
```powershell
Get-Content arquivo.txt
```

### Ver Primeiras Linhas
```powershell
Get-Content arquivo.txt -Head 10
```

### Ver Últimas Linhas
```powershell
Get-Content arquivo.txt -Tail 10
```

---

## 🌐 Rede

### Ver Processos Usando Porta 8501
```powershell
netstat -ano | findstr :8501
```

### Matar Processo por PID
```powershell
taskkill /PID <número_do_pid> /F
```

---

## 💡 Atalhos Úteis

### Parar Servidor Streamlit
`Ctrl + C` no terminal

### Limpar Terminal
```powershell
cls
```

### Histórico de Comandos
Setas ↑ e ↓

---

## 📝 Dicas

### Executar Múltiplos Comandos em Sequência
```powershell
comando1; comando2; comando3
```

### Redirecionar Saída para Arquivo
```powershell
comando > saida.txt
```

### Adicionar Saída ao Arquivo (Append)
```powershell
comando >> saida.txt
```

---

**Referência rápida para comandos do dia a dia! 💻**
