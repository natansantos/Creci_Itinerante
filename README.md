# 🗺️ CRECI Itinerante - Sistema de BI Geográfico

Sistema de Business Intelligence para planejamento de rotas de visita ao interior da Bahia, desenvolvido para o CRECI.

**🔐 NOVO: Sistema com autenticação e integração segura com Google Sheets**

## 📋 Funcionalidades

- 🔐 **Autenticação Segura**: Sistema de login com hash bcrypt para proteger acesso
- 📊 **Google Sheets Integration**: Dados carregados de planilhas privadas do Google Sheets
- ✅ **Fuzzy Matching Inteligente**: Normalização automática de nomes de cidades com erros de digitação
- 🗺️ **Visualização Interativa**: Mapa com marcadores coloridos baseados em quantidade de profissionais
- 📊 **KPIs em Tempo Real**: Métricas consolidadas de corretores e imobiliárias
- 🔍 **Filtros Dinâmicos**: Filtragem por quantidade mínima de profissionais
- 📈 **Top 10 Cidades**: Ranking das cidades com mais profissionais
- 📋 **Tabela Detalhada**: Exportação e visualização dos dados consolidados

## 🚀 Como Executar

### ⚡ Início Rápido

Consulte o [INICIO_RAPIDO.md](INICIO_RAPIDO.md) para instruções passo a passo.

### 1. Instalar Dependências

```powershell
# Ativar ambiente virtual
.\.venv\Scripts\Activate.ps1

# Instalar dependências
pip install -r requirements.txt
```

### 2. Configurar Sistema

```powershell
# Gerar hash da senha
python gerar_senha.py

# Copiar e preencher arquivo de configuração
Copy-Item .env.example .env
# Edite o arquivo .env com suas credenciais
```

Para configuração completa do Google Sheets API, consulte [GUIA_CONFIGURACAO.md](GUIA_CONFIGURACAO.md).

### 3. Executar o Sistema

```powershell
streamlit run app.py
```

O sistema abrirá automaticamente no navegador em `http://localhost:8501`

## 📁 Estrutura de Arquivos

```
Creci_Itinerante/
├── app.py                      # Aplicação principal Streamlit
├── auth.py                     # Módulo de autenticação
├── google_sheets.py            # Integração com Google Sheets API
├── gerar_senha.py              # Script para gerar hash de senhas
├── requirements.txt            # Dependências Python
├── .env.example                # Template de configuração
├── .env                        # Configurações (NÃO versionar)
├── google_credentials.json     # Credenciais Google (NÃO versionar)
├── README.md                   # Esta documentação
├── INICIO_RAPIDO.md            # Guia rápido de execução
├── GUIA_CONFIGURACAO.md        # Guia completo de configuração
├── GUIA_EXECUCAO.md            # Guia de execução (legado)
└── dados/
    ├── municipios.json         # Base de municípios do Brasil
    ├── Corretores.xlsx         # [OPCIONAL] Backup local
    └── Imobiliárias.xlsx       # [OPCIONAL] Backup local
```

## 📊 Formato dos Dados

### Planilhas do Google Sheets

As planilhas devem ter as seguintes colunas:
- `CIDADE`: Nome da cidade
- `UF`: Unidade federativa (deve ser "BA" ou "Bahia")
- `QUANTIDADE`: Quantidade total
- `REGULAR`: Quantidade de profissionais regulares
- `IRREGULAR`: Quantidade de profissionais irregulares

### municipios.json

O sistema filtra automaticamente apenas municípios da Bahia (`codigo_uf == 29`).

## 🔐 Segurança

- ✅ Autenticação com hash bcrypt
- ✅ Credenciais em variáveis de ambiente (.env)
- ✅ Dados sensíveis não versionados no Git
- ✅ Google Sheets com acesso restrito por Service Account
- ✅ Sessões seguras do Streamlit

## 🎨 Interface

### Tela de Login
- Sistema de autenticação com usuário e senha
- Validação segura com hash bcrypt

### Sidebar (Filtros)
- **Informações do usuário logado**
- **Botão de logout**
- **Quantidade Mínima de Corretores**: Filtra cidades com pelo menos X corretores
- **Quantidade Mínima de Imobiliárias**: Filtra cidades com pelo menos X imobiliárias

### Dashboard Principal
- **Indicadores Gerais**: 5 métricas principais (cidades, profissionais, corretores, imobiliárias, média)
- **Situação Cadastral**: Distribuição entre regulares e irregulares
- **Mapa Interativo**: Visualização geográfica com popups detalhados
- **Top 10 Cidades**: Ranking das principais cidades
- **Tabela Detalhada**: Dados completos em formato tabular

### Cores dos Marcadores no Mapa
- 🔴 **Vermelho** (Estrela): ≥ 100 profissionais
- 🟠 **Laranja** (Info): 50-99 profissionais
- 🔵 **Azul** (Usuário): 20-49 profissionais
- 🟢 **Verde** (Pin): < 20 profissionais

## 🔧 Tecnologias Utilizadas

- **Streamlit**: Framework web para dashboards interativos
- **Google Sheets API**: Integração segura com planilhas privadas
- **Pandas**: Manipulação e análise de dados
- **Folium**: Mapas interativos
- **RapidFuzz**: Fuzzy matching para normalização de nomes
- **bcrypt**: Hash seguro de senhas
- **gspread**: Cliente Python para Google Sheets
- **python-dotenv**: Gerenciamento de variáveis de ambiente

## 🧪 Tratamento de Dados

O sistema implementa:

1. **Normalização de Nomes**: Conversão para maiúsculas e remoção de espaços extras
2. **Fuzzy Matching**: Score de similaridade > 85% para associar cidades com erros de digitação
3. **Consolidação de Duplicatas**: Soma automática de cidades repetidas
4. **Validação de Colunas**: Verificação de colunas essenciais e criação de colunas faltantes
5. **Tratamento de Exceções**: Mensagens de erro claras para problemas de dados
6. **Cache Inteligente**: Dados do Google Sheets em cache por 5 minutos
7. **Fallback para Excel**: Sistema usa arquivos locais se Google Sheets falhar

## 📈 Melhorias Futuras

- [ ] Exportação de dados filtrados para Excel
- [ ] Cálculo de rotas otimizadas entre cidades
- [ ] Análise temporal (se houver dados históricos)
- [ ] Previsão de crescimento por região
- [ ] Integração com APIs de mapas para cálculo de distâncias
- [ ] Sistema multi-usuário com roles (admin, visualizador, etc.)
- [ ] Registro de auditoria (logs de acesso)

## 👨‍💻 Autor

Desenvolvido por Natan Santos  
Janeiro de 2026

## 📄 Licença

Sistema proprietário para uso interno do CRECI.
