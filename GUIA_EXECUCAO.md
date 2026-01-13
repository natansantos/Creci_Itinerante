# 🚀 Guia Rápido de Execução - CRECI Itinerante

## Para Iniciar o Sistema

Execute o seguinte comando no PowerShell:

```powershell
streamlit run app.py
```

O sistema abrirá automaticamente no navegador em: **http://localhost:8501**

---

## 📌 Estrutura do Código

### Principais Funções:

1. **`carregar_municipios_bahia()`**
   - Carrega o JSON de municípios
   - Filtra apenas Bahia (codigo_uf == 29)
   - Normaliza nomes para maiúsculas

2. **`carregar_excel()`**
   - Lê arquivos Excel de Corretores e Imobiliárias
   - Filtra apenas UF = "BA"
   - Consolida duplicatas por cidade
   - Trata valores ausentes

3. **`realizar_fuzzy_matching()`**
   - Tenta match exato primeiro
   - Se falhar, usa RapidFuzz com threshold de 85%
   - Associa cidades dos Excel com o JSON

4. **`consolidar_dados()`**
   - Unifica dados de Corretores e Imobiliárias
   - Aplica fuzzy matching para cada cidade
   - Adiciona coordenadas geográficas
   - Calcula totais combinados

5. **`criar_mapa()`**
   - Gera mapa interativo com Folium
   - Marcadores coloridos por quantidade de profissionais
   - Popups HTML com detalhes completos

---

## 🎨 Personalização

### Alterar Threshold do Fuzzy Matching

No arquivo [app.py](app.py), linha 24:

```python
FUZZY_THRESHOLD = 85  # Altere este valor (0-100)
```

### Alterar Centro do Mapa

No arquivo [app.py](app.py), linha 25:

```python
COORDENADAS_CENTRO_BAHIA = (-12.5797, -41.7007)  # (latitude, longitude)
```

### Cores dos Marcadores

No arquivo [app.py](app.py), função `criar_mapa()`, linhas ~293-304:

```python
if row['total_profissionais'] >= 100:
    cor = 'red'      # Altere aqui
    icone = 'star'
elif row['total_profissionais'] >= 50:
    cor = 'orange'   # Altere aqui
    icone = 'info-sign'
# ...
```

Cores disponíveis: 'red', 'blue', 'green', 'purple', 'orange', 'darkred', 'lightred', 'beige', 'darkblue', 'darkgreen', 'cadetblue', 'darkpurple', 'white', 'pink', 'lightblue', 'lightgreen', 'gray', 'black', 'lightgray'

---

## 🔍 Resolução de Problemas

### Erro: "Arquivo não encontrado"
- Verifique se os arquivos estão na pasta `dados/`
- Nomes corretos: `Corretores.xlsx`, `Imobiliárias.xlsx`, `municipios.json`

### Erro: "Colunas faltantes"
- Verifique se os Excel possuem as colunas: CIDADE, UF, QUANTIDADE, REGULAR, IRREGULAR
- O sistema tolera variações, mas os nomes devem ser similares

### Fuzzy Matching não encontra cidades
- Reduza o threshold (padrão: 85%)
- Verifique se os nomes no Excel estão muito diferentes
- Use a tabela detalhada para ver quais cidades não foram mapeadas

### Mapa não carrega
- Verifique sua conexão com a internet (Folium usa tiles do OpenStreetMap)
- Tente recarregar a página (F5)

---

## 📊 Interpretação dos Dados

### KPIs Principais:
- **Cidades Mapeadas**: Número de cidades que atendem aos filtros atuais
- **Total Profissionais**: Soma de corretores + imobiliárias
- **Média por Cidade**: Média de profissionais por cidade filtrada

### Marcadores no Mapa:
- **Tamanho não varia**, apenas cor e ícone
- **Clique no marcador** para ver detalhes completos
- **Passe o mouse** para preview rápido

---

## 🛠️ Tecnologias Utilizadas

- **Python 3.13+**
- **Streamlit**: Framework web para dashboards
- **Pandas**: Manipulação de dados
- **Folium**: Mapas interativos
- **RapidFuzz**: Fuzzy string matching
- **OpenPyXL**: Leitura de Excel

---

## 📝 Notas Técnicas

1. **Cache de Dados**: O sistema usa `@st.cache_data` para melhorar performance. Os dados são carregados apenas uma vez.

2. **Fuzzy Matching**: Usa algoritmo WRatio (Weighted Ratio) do RapidFuzz, que é mais robusto para nomes com erros.

3. **Normalização**: Todos os nomes são convertidos para maiúsculas e espaços extras são removidos.

4. **Consolidação de Duplicatas**: Se houver múltiplas entradas para a mesma cidade, as quantidades são somadas.

---

## 🔄 Atualizando os Dados

Para atualizar os dados:

1. Substitua os arquivos Excel na pasta `dados/`
2. Mantenha os mesmos nomes e estrutura de colunas
3. Recarregue a página ou reinicie o Streamlit

O sistema detectará automaticamente as alterações (graças ao cache do Streamlit).

---

**Desenvolvido com 💙 por Engenheiro de Dados Sênior**  
Janeiro 2026
