# 🗺️ CRECI Itinerante - Sistema de BI Geográfico

Sistema de Business Intelligence para planejamento de rotas de visita ao interior da Bahia, desenvolvido para o CRECI.

## 📋 Funcionalidades

- ✅ **Fuzzy Matching Inteligente**: Normalização automática de nomes de cidades com erros de digitação
- 🗺️ **Visualização Interativa**: Mapa com marcadores coloridos baseados em quantidade de profissionais
- 📊 **KPIs em Tempo Real**: Métricas consolidadas de corretores e imobiliárias
- 🔍 **Filtros Dinâmicos**: Filtragem por quantidade mínima de profissionais
- 📈 **Top 10 Cidades**: Ranking das cidades com mais profissionais
- 📋 **Tabela Detalhada**: Exportação e visualização dos dados consolidados

## 🚀 Como Executar

### 1. Instalar Dependências

```powershell
pip install -r requirements.txt
```

### 2. Executar o Sistema

```powershell
streamlit run app.py
```

O sistema abrirá automaticamente no navegador em `http://localhost:8501`

## 📁 Estrutura de Arquivos

```
Creci_Itinerante/
├── app.py                      # Aplicação principal Streamlit
├── requirements.txt            # Dependências Python
├── README.md                   # Esta documentação
└── dados/
    ├── municipios.json         # Base de municípios do Brasil
    ├── Corretores.xlsx         # Dados de corretores da Bahia
    └── Imobiliárias.xlsx       # Dados de imobiliárias da Bahia
```

## 📊 Formato dos Dados

### Arquivos Excel (Corretores.xlsx e Imobiliárias.xlsx)

Colunas esperadas:
- `CIDADE`: Nome da cidade
- `UF`: Unidade federativa (deve ser "BA" ou "Bahia")
- `QUANTIDADE`: Quantidade total
- `REGULAR`: Quantidade regular
- `IRREGULAR`: Quantidade irregular

### municipios.json

O sistema filtra automaticamente apenas municípios da Bahia (`codigo_uf == 29`).

## 🎨 Interface

### Sidebar (Filtros)
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
- **Pandas**: Manipulação e análise de dados
- **Folium**: Mapas interativos
- **RapidFuzz**: Fuzzy matching para normalização de nomes
- **OpenPyXL**: Leitura de arquivos Excel

## 🧪 Tratamento de Dados

O sistema implementa:

1. **Normalização de Nomes**: Conversão para maiúsculas e remoção de espaços extras
2. **Fuzzy Matching**: Score de similaridade > 85% para associar cidades com erros de digitação
3. **Consolidação de Duplicatas**: Soma automática de cidades repetidas
4. **Validação de Colunas**: Verificação de colunas essenciais e criação de colunas faltantes
5. **Tratamento de Exceções**: Mensagens de erro claras para problemas de dados

## 📈 Melhorias Futuras

- [ ] Exportação de dados filtrados para Excel
- [ ] Cálculo de rotas otimizadas entre cidades
- [ ] Análise temporal (se houver dados históricos)
- [ ] Previsão de crescimento por região
- [ ] Integração com APIs de mapas para cálculo de distâncias

## 👨‍💻 Autor

Desenvolvido por Natan Santos  
Janeiro de 2026

## 📄 Licença

Sistema proprietário para uso interno do CRECI.
