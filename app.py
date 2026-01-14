"""
Sistema CRECI Itinerante - Business Intelligence Geográfico
Planejamento de Rotas de Visita ao Interior da Bahia

Autor: Engenheiro de Dados Sênior
Data: Janeiro 2026

NOVO: Sistema com autenticação e integração com Google Sheets
"""

import streamlit as st
import pandas as pd
import json
import folium
from streamlit_folium import st_folium
from rapidfuzz import fuzz, process
import os
from pathlib import Path

# Importar módulos de autenticação e Google Sheets
from auth import Authenticator
from google_sheets import get_sheets_loader

# =====================================================================
# CONFIGURAÇÃO DA PÁGINA
# =====================================================================
st.set_page_config(
    page_title="CRECI Itinerante - Bahia",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================================
# CONSTANTES
# =====================================================================
CODIGO_UF_BAHIA = 29
FUZZY_THRESHOLD = 85
COORDENADAS_CENTRO_BAHIA = (-12.5797, -41.7007)  # Centro aproximado da BA

# =====================================================================
# FUNÇÕES DE CARREGAMENTO E PROCESSAMENTO
# =====================================================================

@st.cache_data
def carregar_municipios_bahia():
    """
    Carrega o arquivo JSON de municípios e filtra apenas os da Bahia.
    
    Returns:
        DataFrame com municípios da Bahia e suas coordenadas.
    """
    try:
        caminho_json = Path("dados/municipios.json")
        
        with open(caminho_json, 'r', encoding='utf-8-sig') as f:
            municipios = json.load(f)
        
        # Filtrar apenas municípios da Bahia
        municipios_ba = [m for m in municipios if m.get('codigo_uf') == CODIGO_UF_BAHIA]
        
        df = pd.DataFrame(municipios_ba)
        
        # Normalizar nomes para facilitar matching
        df['nome_normalizado'] = df['nome'].str.upper().str.strip()
        
        st.sidebar.success(f"✅ {len(df)} municípios da Bahia carregados")
        
        return df
        
    except FileNotFoundError:
        st.error("❌ Arquivo municipios.json não encontrado!")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"❌ Erro ao carregar municípios: {str(e)}")
        return pd.DataFrame()


@st.cache_data
def carregar_excel(arquivo, nome_tipo):
    """
    [MODO LEGADO] Carrega e processa arquivo Excel de Corretores ou Imobiliárias.
    Mantido como fallback caso Google Sheets não esteja disponível.
    
    Args:
        arquivo: Nome do arquivo Excel.
        nome_tipo: Tipo de dado ("Corretores" ou "Imobiliárias").
    
    Returns:
        DataFrame processado e normalizado.
    """
    try:
        caminho = Path(f"dados/{arquivo}")
        
        if not caminho.exists():
            return pd.DataFrame()
        
        df = pd.read_excel(caminho)
        
        # Normalizar nomes de colunas (remover espaços extras, dois-pontos finais, maiúsculas)
        df.columns = df.columns.str.strip().str.rstrip(':').str.upper()
        
        # Verificar colunas essenciais
        colunas_esperadas = ['CIDADE', 'UF']
        colunas_faltantes = [col for col in colunas_esperadas if col not in df.columns]
        
        if colunas_faltantes:
            st.warning(f"⚠️ Colunas faltantes em {arquivo}: {colunas_faltantes}")
            return pd.DataFrame()
        
        # Filtrar apenas Bahia
        df = df[df['UF'].str.upper().isin(['BA', 'BAHIA'])].copy()
        
        # Normalizar nomes de cidades
        df['CIDADE_NORMALIZADA'] = df['CIDADE'].str.upper().str.strip()
        
        # Garantir que colunas numéricas existam
        for col in ['QUANTIDADE', 'REGULAR', 'IRREGULAR']:
            if col not in df.columns:
                df[col] = 0
            else:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)
        
        # Consolidar duplicatas (somar quantidades)
        df_consolidado = df.groupby('CIDADE_NORMALIZADA', as_index=False).agg({
            'QUANTIDADE': 'sum',
            'REGULAR': 'sum',
            'IRREGULAR': 'sum'
        })
        
        return df_consolidado
        
    except FileNotFoundError:
        return pd.DataFrame()
    except Exception as e:
        st.error(f"❌ Erro ao carregar {arquivo}: {str(e)}")
        return pd.DataFrame()


def carregar_dados_fonte():
    """
    Carrega dados de corretores e imobiliárias da fonte configurada.
    Prioriza Google Sheets, mas usa Excel local como fallback.
    
    Returns:
        Tupla (df_corretores, df_imobiliarias)
    """
    sheets_loader = get_sheets_loader()
    
    # Tentar carregar do Google Sheets primeiro
    st.sidebar.info("📡 Conectando ao Google Sheets...")
    
    df_corretores = sheets_loader.carregar_corretores()
    df_imobiliarias = sheets_loader.carregar_imobiliarias()
    
    # Se falhar, tentar carregar dos arquivos Excel locais (fallback)
    if df_corretores.empty:
        st.sidebar.warning("⚠️ Tentando carregar corretores do arquivo local...")
        df_corretores = carregar_excel("Corretores.xlsx", "Corretores")
    
    if df_imobiliarias.empty:
        st.sidebar.warning("⚠️ Tentando carregar imobiliárias do arquivo local...")
        df_imobiliarias = carregar_excel("Imobiliárias.xlsx", "Imobiliárias")
    
    return df_corretores, df_imobiliarias


def realizar_fuzzy_matching(nome_cidade, lista_municipios, threshold=FUZZY_THRESHOLD):
    """
    Realiza fuzzy matching para encontrar o município mais próximo.
    
    Args:
        nome_cidade: Nome da cidade a buscar.
        lista_municipios: Lista de nomes normalizados dos municípios.
        threshold: Score mínimo de similaridade (0-100).
    
    Returns:
        Nome do município correspondente ou None.
    """
    try:
        # Tenta match exato primeiro
        if nome_cidade in lista_municipios:
            return nome_cidade
        
        # Se não houver match exato, usa fuzzy matching
        resultado = process.extractOne(
            nome_cidade, 
            lista_municipios, 
            scorer=fuzz.WRatio
        )
        
        if resultado and resultado[1] >= threshold:
            return resultado[0]
        
        return None
        
    except Exception as e:
        st.warning(f"Erro no fuzzy matching para '{nome_cidade}': {str(e)}")
        return None


@st.cache_data
def consolidar_dados(df_municipios, df_corretores, df_imobiliarias):
    """
    Consolida todos os dados em um DataFrame único com coordenadas.
    
    Args:
        df_municipios: DataFrame com municípios e coordenadas.
        df_corretores: DataFrame com dados de corretores.
        df_imobiliarias: DataFrame com dados de imobiliárias.
    
    Returns:
        DataFrame consolidado final.
    """
    try:
        # Criar lista de nomes normalizados dos municípios para fuzzy matching
        municipios_nomes = df_municipios['nome_normalizado'].tolist()
        
        # Processar Corretores
        dados_consolidados = []
        
        # Adicionar dados de corretores
        for _, row in df_corretores.iterrows():
            cidade_match = realizar_fuzzy_matching(row['CIDADE_NORMALIZADA'], municipios_nomes)
            
            if cidade_match:
                municipio_info = df_municipios[df_municipios['nome_normalizado'] == cidade_match].iloc[0]
                
                dados_consolidados.append({
                    'cidade': municipio_info['nome'],
                    'latitude': municipio_info['latitude'],
                    'longitude': municipio_info['longitude'],
                    'corretores_total': row['QUANTIDADE'],
                    'corretores_regulares': row['REGULAR'],
                    'corretores_irregulares': row['IRREGULAR'],
                    'imobiliarias_total': 0,
                    'imobiliarias_regulares': 0,
                    'imobiliarias_irregulares': 0
                })
        
        # Criar DataFrame intermediário
        df_consolidado = pd.DataFrame(dados_consolidados)
        
        # Adicionar dados de imobiliárias
        for _, row in df_imobiliarias.iterrows():
            cidade_match = realizar_fuzzy_matching(row['CIDADE_NORMALIZADA'], municipios_nomes)
            
            if cidade_match:
                municipio_info = df_municipios[df_municipios['nome_normalizado'] == cidade_match].iloc[0]
                cidade_nome = municipio_info['nome']
                
                # Verificar se a cidade já existe no DataFrame
                if cidade_nome in df_consolidado['cidade'].values:
                    # Atualizar dados existentes
                    idx = df_consolidado[df_consolidado['cidade'] == cidade_nome].index[0]
                    df_consolidado.at[idx, 'imobiliarias_total'] = row['QUANTIDADE']
                    df_consolidado.at[idx, 'imobiliarias_regulares'] = row['REGULAR']
                    df_consolidado.at[idx, 'imobiliarias_irregulares'] = row['IRREGULAR']
                else:
                    # Adicionar nova linha
                    df_consolidado = pd.concat([df_consolidado, pd.DataFrame([{
                        'cidade': cidade_nome,
                        'latitude': municipio_info['latitude'],
                        'longitude': municipio_info['longitude'],
                        'corretores_total': 0,
                        'corretores_regulares': 0,
                        'corretores_irregulares': 0,
                        'imobiliarias_total': row['QUANTIDADE'],
                        'imobiliarias_regulares': row['REGULAR'],
                        'imobiliarias_irregulares': row['IRREGULAR']
                    }])], ignore_index=True)
        
        # Calcular totais combinados
        df_consolidado['total_profissionais'] = (
            df_consolidado['corretores_total'] + 
            df_consolidado['imobiliarias_total']
        )
        
        # Ordenar por total de profissionais (decrescente)
        df_consolidado = df_consolidado.sort_values('total_profissionais', ascending=False)
        
        return df_consolidado.reset_index(drop=True)
        
    except Exception as e:
        st.error(f"❌ Erro ao consolidar dados: {str(e)}")
        return pd.DataFrame()


def criar_popup_html(row):
    """
    Cria HTML formatado para o popup do marcador no mapa.
    
    Args:
        row: Linha do DataFrame com dados da cidade.
    
    Returns:
        String HTML formatada.
    """
    html = f"""
    <div style="font-family: Arial, sans-serif; width: 300px;">
        <h3 style="margin: 0 0 10px 0; color: #1f77b4; border-bottom: 2px solid #1f77b4; padding-bottom: 5px;">
            📍 {row['cidade']}
        </h3>
        
        <div style="margin: 10px 0;">
            <h4 style="margin: 5px 0; color: #2ca02c;">👤 Corretores</h4>
            <table style="width: 100%; border-collapse: collapse;">
                <tr>
                    <td style="padding: 3px;"><strong>Total:</strong></td>
                    <td style="padding: 3px; text-align: right;">{int(row['corretores_total'])}</td>
                </tr>
                <tr style="background-color: #e8f5e9;">
                    <td style="padding: 3px;">✅ Regulares:</td>
                    <td style="padding: 3px; text-align: right;">{int(row['corretores_regulares'])}</td>
                </tr>
                <tr style="background-color: #ffebee;">
                    <td style="padding: 3px;">⚠️ Irregulares:</td>
                    <td style="padding: 3px; text-align: right;">{int(row['corretores_irregulares'])}</td>
                </tr>
            </table>
        </div>
        
        <div style="margin: 10px 0;">
            <h4 style="margin: 5px 0; color: #ff7f0e;">🏢 Imobiliárias</h4>
            <table style="width: 100%; border-collapse: collapse;">
                <tr>
                    <td style="padding: 3px;"><strong>Total:</strong></td>
                    <td style="padding: 3px; text-align: right;">{int(row['imobiliarias_total'])}</td>
                </tr>
                <tr style="background-color: #e8f5e9;">
                    <td style="padding: 3px;">✅ Regulares:</td>
                    <td style="padding: 3px; text-align: right;">{int(row['imobiliarias_regulares'])}</td>
                </tr>
                <tr style="background-color: #ffebee;">
                    <td style="padding: 3px;">⚠️ Irregulares:</td>
                    <td style="padding: 3px; text-align: right;">{int(row['imobiliarias_irregulares'])}</td>
                </tr>
            </table>
        </div>
        
        <div style="margin-top: 10px; padding-top: 10px; border-top: 1px solid #ccc;">
            <strong>Total de Profissionais: {int(row['total_profissionais'])}</strong>
        </div>
    </div>
    """
    return html


def criar_mapa(df_filtrado):
    """
    Cria o mapa interativo com os marcadores das cidades.
    
    Args:
        df_filtrado: DataFrame com dados filtrados para exibir.
    
    Returns:
        Objeto folium.Map.
    """
    # Criar mapa base
    mapa = folium.Map(
        location=COORDENADAS_CENTRO_BAHIA,
        zoom_start=7,
        tiles='OpenStreetMap'
    )
    
    # Adicionar marcadores
    for _, row in df_filtrado.iterrows():
        # Definir cor do marcador baseado na quantidade de profissionais
        if row['total_profissionais'] >= 100:
            cor = 'red'
            icone = 'star'
        elif row['total_profissionais'] >= 50:
            cor = 'orange'
            icone = 'info-sign'
        elif row['total_profissionais'] >= 20:
            cor = 'blue'
            icone = 'user'
        else:
            cor = 'green'
            icone = 'map-marker'
        
        # Criar popup HTML
        popup_html = criar_popup_html(row)
        
        # Adicionar marcador
        folium.Marker(
            location=[row['latitude'], row['longitude']],
            popup=folium.Popup(popup_html, max_width=350),
            tooltip=f"{row['cidade']} ({int(row['total_profissionais'])} profissionais)",
            icon=folium.Icon(color=cor, icon=icone, prefix='glyphicon')
        ).add_to(mapa)
    
    return mapa


# =====================================================================
# INTERFACE PRINCIPAL
# =====================================================================

def main():
    """Função principal da aplicação Streamlit."""
    
    # ============================================
    # AUTENTICAÇÃO
    # ============================================
    authenticator = Authenticator()
    
    # Verificar se o usuário está autenticado
    if not authenticator.is_authenticated():
        # Mostrar formulário de login
        authenticator.login_form()
        return  # Não continuar até fazer login
    
    # ============================================
    # USUÁRIO AUTENTICADO - MOSTRAR APLICAÇÃO
    # ============================================
    
    # Cabeçalho com informações do usuário
    user = authenticator.get_current_user()
    col_title, col_user = st.columns([4, 1])
    
    with col_title:
        st.title("🗺️ CRECI Itinerante - Bahia")
        st.markdown("**Sistema de Business Intelligence Geográfico para Planejamento de Rotas**")
    
    with col_user:
        st.write("")  # Espaçamento
        st.write(f"👤 **{user['name']}**")
        if st.button("🚪 Sair", use_container_width=True):
            authenticator.logout()
    
    st.markdown("---")
    
    # Sidebar - Filtros
    st.sidebar.title("⚙️ Configurações")
    st.sidebar.markdown("---")
    
    # Carregar dados
    with st.spinner("📊 Carregando dados..."):
        df_municipios = carregar_municipios_bahia()
        df_corretores, df_imobiliarias = carregar_dados_fonte()
    
    # Verificar se os dados foram carregados
    if df_municipios.empty or df_corretores.empty or df_imobiliarias.empty:
        st.error("❌ Não foi possível carregar todos os dados necessários.")
        st.info("💡 Verifique as configurações do Google Sheets no arquivo .env")
        
        # Mostrar botão para recarregar
        if st.button("🔄 Tentar Novamente"):
            st.rerun()
        return
    
    # Consolidar dados
    with st.spinner("🔄 Processando e consolidando dados..."):
        df_consolidado = consolidar_dados(df_municipios, df_corretores, df_imobiliarias)
    
    if df_consolidado.empty:
        st.error("❌ Não foi possível consolidar os dados.")
        return
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("🔍 Filtros de Visualização")
    
    # Filtro de quantidade mínima de corretores
    min_corretores = st.sidebar.number_input(
        "Quantidade Mínima de Corretores",
        min_value=0,
        max_value=int(df_consolidado['corretores_total'].max()),
        value=0,
        step=5,
        help="Filtre cidades com pelo menos este número de corretores"
    )
    
    # Filtro adicional de imobiliárias
    min_imobiliarias = st.sidebar.number_input(
        "Quantidade Mínima de Imobiliárias",
        min_value=0,
        max_value=int(df_consolidado['imobiliarias_total'].max()),
        value=0,
        step=5,
        help="Filtre cidades com pelo menos este número de imobiliárias"
    )
    
    # Aplicar filtros
    df_filtrado = df_consolidado[
        (df_consolidado['corretores_total'] >= min_corretores) &
        (df_consolidado['imobiliarias_total'] >= min_imobiliarias)
    ].copy()
    
    # KPIs
    st.subheader("📊 Indicadores Gerais")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric(
            "🏙️ Cidades Mapeadas",
            len(df_filtrado),
            f"{len(df_filtrado)/len(df_consolidado)*100:.1f}% do total"
        )
    
    with col2:
        st.metric(
            "👥 Total Profissionais",
            f"{int(df_filtrado['total_profissionais'].sum()):,}",
            help="Soma de corretores e imobiliárias"
        )
    
    with col3:
        st.metric(
            "👤 Total Corretores",
            f"{int(df_filtrado['corretores_total'].sum()):,}"
        )
    
    with col4:
        st.metric(
            "🏢 Total Imobiliárias",
            f"{int(df_filtrado['imobiliarias_total'].sum()):,}"
        )
    
    with col5:
        media_prof = df_filtrado['total_profissionais'].mean() if len(df_filtrado) > 0 else 0
        st.metric(
            "📈 Média por Cidade",
            f"{int(media_prof)}"
        )
    
    st.markdown("---")
    
    # Distribuição Regular vs Irregular
    col_reg1, col_reg2 = st.columns(2)
    
    with col_reg1:
        st.subheader("✅ Corretores - Situação")
        cor_reg = int(df_filtrado['corretores_regulares'].sum())
        cor_irreg = int(df_filtrado['corretores_irregulares'].sum())
        total_cor = cor_reg + cor_irreg
        
        if total_cor > 0:
            st.write(f"**Regulares:** {cor_reg:,} ({cor_reg/total_cor*100:.1f}%)")
            st.write(f"**Irregulares:** {cor_irreg:,} ({cor_irreg/total_cor*100:.1f}%)")
            st.progress(cor_reg / total_cor)
        else:
            st.info("Sem dados de corretores")
    
    with col_reg2:
        st.subheader("✅ Imobiliárias - Situação")
        imob_reg = int(df_filtrado['imobiliarias_regulares'].sum())
        imob_irreg = int(df_filtrado['imobiliarias_irregulares'].sum())
        total_imob = imob_reg + imob_irreg
        
        if total_imob > 0:
            st.write(f"**Regulares:** {imob_reg:,} ({imob_reg/total_imob*100:.1f}%)")
            st.write(f"**Irregulares:** {imob_irreg:,} ({imob_irreg/total_imob*100:.1f}%)")
            st.progress(imob_reg / total_imob)
        else:
            st.info("Sem dados de imobiliárias")
    
    st.markdown("---")
    
    # Mapa
    st.subheader("🗺️ Visualização Geográfica")
    
    if len(df_filtrado) == 0:
        st.warning("⚠️ Nenhuma cidade atende aos critérios de filtro selecionados.")
    else:
        with st.spinner("🗺️ Gerando mapa interativo..."):
            mapa = criar_mapa(df_filtrado)
            st_folium(mapa, width=None, height=800, use_container_width=True)
    
    st.markdown("---")
    
    # Tabela de dados
    with st.expander("📋 Ver Tabela de Dados Detalhada"):
        st.dataframe(
            df_filtrado[[
                'cidade', 'corretores_total', 'corretores_regulares', 
                'corretores_irregulares', 'imobiliarias_total', 
                'imobiliarias_regulares', 'imobiliarias_irregulares',
                'total_profissionais'
            ]].rename(columns={
                'cidade': 'Cidade',
                'corretores_total': 'Corretores (Total)',
                'corretores_regulares': 'Corretores (Regulares)',
                'corretores_irregulares': 'Corretores (Irregulares)',
                'imobiliarias_total': 'Imobiliárias (Total)',
                'imobiliarias_regulares': 'Imobiliárias (Regulares)',
                'imobiliarias_irregulares': 'Imobiliárias (Irregulares)',
                'total_profissionais': 'Total Profissionais'
            }),
            use_container_width=True,
            height=400
        )
    
    # Top 10 cidades
    st.subheader("🏆 Top 10 Cidades com Mais Profissionais")
    top10 = df_filtrado.nlargest(10, 'total_profissionais')
    
    for idx, row in top10.iterrows():
        col_cidade, col_corretores, col_imobiliarias = st.columns([2, 1, 1])
        
        with col_cidade:
            st.write(f"**{row['cidade']}**")
        
        with col_corretores:
            st.write(f"👤 {int(row['corretores_total'])} corretores")
        
        with col_imobiliarias:
            st.write(f"🏢 {int(row['imobiliarias_total'])} imobiliárias")
    
    # Rodapé
    st.markdown("---")
    st.caption("💼 Sistema CRECI Itinerante | Desenvolvido com Streamlit + Google Sheets + Folium")
    st.caption(f"🔐 Usuário: {user['name']} | 🔒 Sessão Segura")


# =====================================================================
# EXECUÇÃO
# =====================================================================
if __name__ == "__main__":
    main()
