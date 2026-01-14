"""
Módulo de Integração com Google Sheets
Carrega dados de planilhas do Google Sheets de forma segura

Autor: Engenheiro de Dados Sênior
Data: Janeiro 2026
"""

import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pathlib import Path
import os
from dotenv import load_dotenv
from typing import Optional
import time

# Carregar variáveis de ambiente
load_dotenv()


class GoogleSheetsLoader:
    """
    Classe para carregar dados do Google Sheets de forma segura.
    """
    
    def __init__(self):
        """Inicializa o loader com credenciais do .env"""
        self.credentials_file = os.getenv('GOOGLE_CREDENTIALS_FILE', 'google_credentials.json')
        self.sheet_corretores = os.getenv('GOOGLE_SHEET_CORRETORES', '')
        self.sheet_imobiliarias = os.getenv('GOOGLE_SHEET_IMOBILIARIAS', '')
        self.sheet_name_corretores = os.getenv('SHEET_NAME_CORRETORES', 'Corretores')
        self.sheet_name_imobiliarias = os.getenv('SHEET_NAME_IMOBILIARIAS', 'Imobiliárias')
        self.timeout = int(os.getenv('SHEETS_TIMEOUT', '30'))
        
        self.client = None
        self._authenticated = False
    
    
    def authenticate(self) -> bool:
        """
        Autentica com o Google Sheets API usando Service Account.
        
        Returns:
            True se autenticado com sucesso, False caso contrário.
        """
        try:
            # Verificar se o arquivo de credenciais existe
            credentials_path = Path(self.credentials_file)
            
            if not credentials_path.exists():
                st.error(f"❌ Arquivo de credenciais não encontrado: {self.credentials_file}")
                st.info("📖 Consulte o GUIA_CONFIGURACAO.md para obter as credenciais.")
                return False
            
            # Definir o escopo de acesso
            scope = [
                'https://spreadsheets.google.com/feeds',
                'https://www.googleapis.com/auth/drive'
            ]
            
            # Autenticar com as credenciais
            credentials = ServiceAccountCredentials.from_json_keyfile_name(
                str(credentials_path),
                scope
            )
            
            self.client = gspread.authorize(credentials)
            self._authenticated = True
            
            return True
            
        except Exception as e:
            st.error(f"❌ Erro ao autenticar com Google Sheets: {str(e)}")
            return False
    
    
    def _extract_sheet_id(self, url: str) -> Optional[str]:
        """
        Extrai o ID da planilha a partir da URL.
        
        Args:
            url: URL completa da planilha do Google Sheets.
        
        Returns:
            ID da planilha ou None se não conseguir extrair.
        """
        try:
            # URL padrão: https://docs.google.com/spreadsheets/d/SHEET_ID/edit
            if '/d/' in url:
                sheet_id = url.split('/d/')[1].split('/')[0]
                return sheet_id
            return None
        except Exception:
            return None
    
    
    def load_sheet_data(self, sheet_url: str, worksheet_name: str, data_type: str) -> pd.DataFrame:
        """
        Carrega dados de uma planilha do Google Sheets.
        
        Args:
            sheet_url: URL da planilha do Google Sheets.
            worksheet_name: Nome da aba/worksheet dentro da planilha.
            data_type: Tipo de dado (para mensagens de log).
        
        Returns:
            DataFrame com os dados ou DataFrame vazio em caso de erro.
        """
        try:
            # Autenticar se ainda não foi feito
            if not self._authenticated:
                if not self.authenticate():
                    return pd.DataFrame()
            
            # Extrair ID da planilha
            sheet_id = self._extract_sheet_id(sheet_url)
            
            if not sheet_id:
                st.error(f"❌ URL inválida para {data_type}: {sheet_url}")
                return pd.DataFrame()
            
            # Abrir a planilha
            with st.spinner(f"📥 Carregando dados de {data_type} do Google Sheets..."):
                spreadsheet = self.client.open_by_key(sheet_id)
                
                # Tentar abrir a worksheet específica ou a primeira
                try:
                    worksheet = spreadsheet.worksheet(worksheet_name)
                except gspread.WorksheetNotFound:
                    st.warning(f"⚠️ Aba '{worksheet_name}' não encontrada. Usando primeira aba.")
                    worksheet = spreadsheet.get_worksheet(0)
                
                # Carregar todos os dados
                data = worksheet.get_all_records()
                
                if not data:
                    st.warning(f"⚠️ Nenhum dado encontrado em {data_type}")
                    return pd.DataFrame()
                
                df = pd.DataFrame(data)
                
                st.sidebar.success(f"✅ {len(df)} registros de {data_type} carregados do Google Sheets")
                
                return df
                
        except gspread.exceptions.APIError as e:
            st.error(f"❌ Erro na API do Google Sheets para {data_type}: {str(e)}")
            st.info("💡 Verifique se a Service Account tem permissão de acesso à planilha.")
            return pd.DataFrame()
            
        except Exception as e:
            st.error(f"❌ Erro ao carregar {data_type}: {str(e)}")
            return pd.DataFrame()
    
    
    @st.cache_data(ttl=300)  # Cache por 5 minutos
    def carregar_corretores(_self) -> pd.DataFrame:
        """
        Carrega dados de corretores do Google Sheets.
        
        Returns:
            DataFrame com dados de corretores.
        """
        if not _self.sheet_corretores:
            st.error("❌ URL da planilha de Corretores não configurada no .env")
            return pd.DataFrame()
        
        df = _self.load_sheet_data(
            _self.sheet_corretores,
            _self.sheet_name_corretores,
            "Corretores"
        )
        
        return _self._processar_dados(df, "Corretores")
    
    
    @st.cache_data(ttl=300)  # Cache por 5 minutos
    def carregar_imobiliarias(_self) -> pd.DataFrame:
        """
        Carrega dados de imobiliárias do Google Sheets.
        
        Returns:
            DataFrame com dados de imobiliárias.
        """
        if not _self.sheet_imobiliarias:
            st.error("❌ URL da planilha de Imobiliárias não configurada no .env")
            return pd.DataFrame()
        
        df = _self.load_sheet_data(
            _self.sheet_imobiliarias,
            _self.sheet_name_imobiliarias,
            "Imobiliárias"
        )
        
        return _self._processar_dados(df, "Imobiliárias")
    
    
    def _processar_dados(self, df: pd.DataFrame, nome_tipo: str) -> pd.DataFrame:
        """
        Processa e normaliza os dados carregados.
        
        Args:
            df: DataFrame com dados brutos.
            nome_tipo: Tipo de dado (para logs).
        
        Returns:
            DataFrame processado.
        """
        if df.empty:
            return df
        
        try:
            # Normalizar nomes de colunas (remover espaços extras, dois-pontos finais, maiúsculas)
            df.columns = df.columns.str.strip().str.rstrip(':').str.upper()
            
            # Verificar colunas essenciais
            colunas_esperadas = ['CIDADE', 'UF']
            colunas_faltantes = [col for col in colunas_esperadas if col not in df.columns]
            
            if colunas_faltantes:
                st.warning(f"⚠️ Colunas faltantes em {nome_tipo}: {colunas_faltantes}")
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
            
        except Exception as e:
            st.error(f"❌ Erro ao processar dados de {nome_tipo}: {str(e)}")
            return pd.DataFrame()


# Instância global do loader (será inicializada no app.py)
sheets_loader = None


def get_sheets_loader() -> GoogleSheetsLoader:
    """
    Retorna a instância do GoogleSheetsLoader (singleton).
    
    Returns:
        Instância de GoogleSheetsLoader.
    """
    global sheets_loader
    if sheets_loader is None:
        sheets_loader = GoogleSheetsLoader()
    return sheets_loader
