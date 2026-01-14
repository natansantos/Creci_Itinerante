"""
Módulo de Autenticação para Sistema CRECI Itinerante
Gerencia login e controle de acesso ao sistema

Autor: Engenheiro de Dados Sênior
Data: Janeiro 2026
"""

import streamlit as st
import bcrypt
from typing import Optional, Dict
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()


class Authenticator:
    """
    Classe para gerenciar autenticação de usuários no sistema.
    """
    
    def __init__(self):
        """Inicializa o autenticador com credenciais do .env"""
        self.admin_username = os.getenv('ADMIN_USERNAME', 'admin')
        self.admin_password_hash = os.getenv('ADMIN_PASSWORD_HASH', '')
        self.admin_name = os.getenv('ADMIN_NAME', 'Administrador')
        
        # Validar se as credenciais foram configuradas
        if not self.admin_password_hash or self.admin_password_hash == '$2b$12$exemplo_hash_da_senha_aqui':
            st.warning("⚠️ Configure as credenciais no arquivo .env!")
    
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        Verifica se a senha fornecida corresponde ao hash armazenado.
        
        Args:
            plain_password: Senha em texto plano.
            hashed_password: Hash da senha armazenada.
        
        Returns:
            True se a senha é válida, False caso contrário.
        """
        try:
            return bcrypt.checkpw(
                plain_password.encode('utf-8'),
                hashed_password.encode('utf-8')
            )
        except Exception as e:
            st.error(f"Erro ao verificar senha: {str(e)}")
            return False
    
    
    def authenticate(self, username: str, password: str) -> Optional[Dict]:
        """
        Autentica um usuário com nome de usuário e senha.
        
        Args:
            username: Nome de usuário.
            password: Senha em texto plano.
        
        Returns:
            Dicionário com dados do usuário se autenticado, None caso contrário.
        """
        # Verificar credenciais
        if username == self.admin_username:
            if self.verify_password(password, self.admin_password_hash):
                return {
                    'username': self.admin_username,
                    'name': self.admin_name,
                    'role': 'admin'
                }
        
        return None
    
    
    def login_form(self):
        """
        Renderiza o formulário de login e gerencia a sessão.
        
        Returns:
            True se o usuário está autenticado, False caso contrário.
        """
        # Verificar se já está autenticado
        if 'authenticated' in st.session_state and st.session_state.authenticated:
            return True
        
        # Renderizar formulário de login
        st.markdown("""
        <style>
        .login-container {
            max-width: 400px;
            margin: 100px auto;
            padding: 40px;
            background: white;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        </style>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            st.markdown("### 🔐 CRECI Itinerante")
            st.markdown("---")
            
            with st.form("login_form"):
                username = st.text_input("👤 Usuário", key="username_input")
                password = st.text_input("🔑 Senha", type="password", key="password_input")
                
                submit = st.form_submit_button("🚪 Entrar", use_container_width=True)
                
                if submit:
                    if username and password:
                        user = self.authenticate(username, password)
                        
                        if user:
                            # Autenticação bem-sucedida
                            st.session_state.authenticated = True
                            st.session_state.user = user
                            st.success("✅ Login realizado com sucesso!")
                            st.rerun()
                        else:
                            st.error("❌ Usuário ou senha inválidos!")
                    else:
                        st.warning("⚠️ Preencha todos os campos!")
            
            st.markdown("---")
            st.caption("Sistema seguro com autenticação 🔒")
        
        return False
    
    
    def logout(self):
        """Realiza o logout do usuário."""
        if 'authenticated' in st.session_state:
            del st.session_state.authenticated
        if 'user' in st.session_state:
            del st.session_state.user
        st.rerun()
    
    
    def get_current_user(self) -> Optional[Dict]:
        """
        Retorna os dados do usuário atualmente autenticado.
        
        Returns:
            Dicionário com dados do usuário ou None.
        """
        if 'user' in st.session_state:
            return st.session_state.user
        return None
    
    
    def is_authenticated(self) -> bool:
        """
        Verifica se há um usuário autenticado.
        
        Returns:
            True se autenticado, False caso contrário.
        """
        return 'authenticated' in st.session_state and st.session_state.authenticated


def generate_password_hash(password: str) -> str:
    """
    Gera um hash bcrypt para uma senha.
    Função utilitária para gerar hashes de senhas.
    
    Args:
        password: Senha em texto plano.
    
    Returns:
        Hash da senha.
    """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')


# Exemplo de uso para gerar hash de senha:
# if __name__ == "__main__":
#     senha = "sua_senha_aqui"
#     hash_gerado = generate_password_hash(senha)
#     print(f"Hash para '{senha}':")
#     print(hash_gerado)
