"""
Módulo de Gerenciamento de Usuários com Banco de Dados
Suporta SQLite local e PostgreSQL remoto (Streamlit Cloud)

Autor: Engenheiro de Dados Sênior
Data: Janeiro 2026
"""

import streamlit as st
import sqlite3
import bcrypt
from pathlib import Path
from typing import Optional, Dict, List
import os
from dotenv import load_dotenv

load_dotenv()


class UserDatabase:
    """
    Gerencia usuários em banco de dados.
    SQLite para desenvolvimento local, PostgreSQL para produção.
    """
    
    def __init__(self):
        """Inicializa conexão com banco de dados"""
        self.db_type = self._get_db_type()
        self.conn = None
        self._initialize_database()
    
    
    def _get_db_type(self) -> str:
        """Determina tipo de banco (sqlite ou postgres)"""
        # Tentar st.secrets primeiro (Streamlit Cloud)
        try:
            if hasattr(st, 'secrets') and st.secrets and 'DATABASE_URL' in st.secrets:
                return 'postgres'
        except:
            pass
        
        # Tentar variável de ambiente (.env local)
        if os.getenv('DATABASE_URL'):
            return 'postgres'
        
        # Padrão: SQLite
        return 'sqlite'
    
    
    def _get_connection(self):
        """Retorna conexão com banco de dados"""
        if self.db_type == 'postgres':
            import psycopg2
            # Obter URL do banco
            db_url = None
            try:
                if hasattr(st, 'secrets') and st.secrets:
                    db_url = st.secrets.get('DATABASE_URL')
            except:
                pass
            
            if not db_url:
                db_url = os.getenv('DATABASE_URL')
            
            return psycopg2.connect(db_url)
        else:
            # SQLite local
            db_path = Path('data/users.db')
            db_path.parent.mkdir(exist_ok=True)
            return sqlite3.connect(str(db_path))
    
    
    def _initialize_database(self):
        """Cria tabela de usuários se não existir"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            if self.db_type == 'postgres':
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        id SERIAL PRIMARY KEY,
                        username VARCHAR(50) UNIQUE NOT NULL,
                        password_hash VARCHAR(255) NOT NULL,
                        full_name VARCHAR(100) NOT NULL,
                        role VARCHAR(20) DEFAULT 'user',
                        active BOOLEAN DEFAULT TRUE,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
            else:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE NOT NULL,
                        password_hash TEXT NOT NULL,
                        full_name TEXT NOT NULL,
                        role TEXT DEFAULT 'user',
                        active INTEGER DEFAULT 1,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
            
            conn.commit()
            conn.close()
            
            # Criar usuário admin padrão se não existir
            self._create_default_admin()
            
        except Exception as e:
            st.error(f"❌ Erro ao inicializar banco de dados: {str(e)}")
    
    
    def _create_default_admin(self):
        """Cria usuário admin padrão se não existir"""
        # Obter credenciais do admin do .env ou secrets
        admin_user = None
        try:
            if hasattr(st, 'secrets') and st.secrets and 'ADMIN_USERNAME' in st.secrets:
                admin_user = st.secrets.get('ADMIN_USERNAME', 'admin')
                admin_hash = st.secrets.get('ADMIN_PASSWORD_HASH', '')
                admin_name = st.secrets.get('ADMIN_NAME', 'Administrador')
        except:
            pass
        
        if not admin_user:
            admin_user = os.getenv('ADMIN_USERNAME', 'admin')
            admin_hash = os.getenv('ADMIN_PASSWORD_HASH', '')
            admin_name = os.getenv('ADMIN_NAME', 'Administrador')
        
        if admin_hash and not self.get_user(admin_user):
            self.create_user(admin_user, admin_hash, admin_name, 'admin', from_hash=True)
    
    
    def create_user(self, username: str, password: str, full_name: str, 
                   role: str = 'user', from_hash: bool = False) -> bool:
        """
        Cria novo usuário.
        
        Args:
            username: Nome de usuário único
            password: Senha em texto plano ou hash (se from_hash=True)
            full_name: Nome completo
            role: Papel do usuário (admin, user)
            from_hash: Se True, password já é um hash
        
        Returns:
            True se criado com sucesso, False caso contrário
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            # Gerar hash da senha se necessário
            if not from_hash:
                password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            else:
                password_hash = password
            
            cursor.execute("""
                INSERT INTO users (username, password_hash, full_name, role)
                VALUES (?, ?, ?, ?)
            """ if self.db_type == 'sqlite' else """
                INSERT INTO users (username, password_hash, full_name, role)
                VALUES (%s, %s, %s, %s)
            """, (username, password_hash, full_name, role))
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            st.error(f"❌ Erro ao criar usuário: {str(e)}")
            return False
    
    
    def get_user(self, username: str) -> Optional[Dict]:
        """
        Busca usuário por username.
        
        Args:
            username: Nome de usuário
        
        Returns:
            Dicionário com dados do usuário ou None
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT id, username, password_hash, full_name, role, active
                FROM users WHERE username = ?
            """ if self.db_type == 'sqlite' else """
                SELECT id, username, password_hash, full_name, role, active
                FROM users WHERE username = %s
            """, (username,))
            
            row = cursor.fetchone()
            conn.close()
            
            if row:
                return {
                    'id': row[0],
                    'username': row[1],
                    'password_hash': row[2],
                    'full_name': row[3],
                    'role': row[4],
                    'active': bool(row[5])
                }
            return None
            
        except Exception as e:
            st.error(f"❌ Erro ao buscar usuário: {str(e)}")
            return None
    
    
    def list_users(self) -> List[Dict]:
        """
        Lista todos os usuários.
        
        Returns:
            Lista de dicionários com dados dos usuários
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT id, username, full_name, role, active, created_at
                FROM users ORDER BY created_at DESC
            """)
            
            rows = cursor.fetchall()
            conn.close()
            
            users = []
            for row in rows:
                users.append({
                    'id': row[0],
                    'username': row[1],
                    'full_name': row[2],
                    'role': row[3],
                    'active': bool(row[4]),
                    'created_at': row[5]
                })
            
            return users
            
        except Exception as e:
            st.error(f"❌ Erro ao listar usuários: {str(e)}")
            return []
    
    
    def update_user(self, username: str, full_name: Optional[str] = None,
                   role: Optional[str] = None, active: Optional[bool] = None) -> bool:
        """
        Atualiza dados do usuário.
        
        Args:
            username: Nome de usuário
            full_name: Novo nome completo (opcional)
            role: Novo papel (opcional)
            active: Novo status (opcional)
        
        Returns:
            True se atualizado com sucesso
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            updates = []
            params = []
            
            if full_name:
                updates.append("full_name = ?" if self.db_type == 'sqlite' else "full_name = %s")
                params.append(full_name)
            
            if role:
                updates.append("role = ?" if self.db_type == 'sqlite' else "role = %s")
                params.append(role)
            
            if active is not None:
                updates.append("active = ?" if self.db_type == 'sqlite' else "active = %s")
                params.append(1 if active else 0)
            
            if not updates:
                return False
            
            params.append(username)
            sql = f"UPDATE users SET {', '.join(updates)} WHERE username = ?" if self.db_type == 'sqlite' else f"UPDATE users SET {', '.join(updates)} WHERE username = %s"
            
            cursor.execute(sql, params)
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            st.error(f"❌ Erro ao atualizar usuário: {str(e)}")
            return False
    
    
    def change_password(self, username: str, new_password: str) -> bool:
        """
        Altera senha do usuário.
        
        Args:
            username: Nome de usuário
            new_password: Nova senha em texto plano
        
        Returns:
            True se alterado com sucesso
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            password_hash = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            
            cursor.execute("""
                UPDATE users SET password_hash = ?
                WHERE username = ?
            """ if self.db_type == 'sqlite' else """
                UPDATE users SET password_hash = %s
                WHERE username = %s
            """, (password_hash, username))
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            st.error(f"❌ Erro ao alterar senha: {str(e)}")
            return False
    
    
    def delete_user(self, username: str) -> bool:
        """
        Deleta usuário (soft delete - marca como inativo).
        
        Args:
            username: Nome de usuário
        
        Returns:
            True se deletado com sucesso
        """
        return self.update_user(username, active=False)


# Instância global
_user_db = None

def get_user_database() -> UserDatabase:
    """Retorna instância singleton do banco de usuários"""
    global _user_db
    if _user_db is None:
        _user_db = UserDatabase()
    return _user_db
