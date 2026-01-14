"""
Interface de Administração de Usuários
Permite criar, editar e gerenciar usuários do sistema

Autor: Engenheiro de Dados Sênior
Data: Janeiro 2026
"""

import streamlit as st
from user_database import get_user_database
from auth import generate_password_hash


def render_user_management():
    """Renderiza interface de gerenciamento de usuários"""
    
    # Verificar se usuário é admin
    if 'user' not in st.session_state or st.session_state.user['role'] != 'admin':
        st.error("❌ Acesso negado. Apenas administradores podem gerenciar usuários.")
        return
    
    st.title("👥 Gerenciamento de Usuários")
    st.markdown("---")
    
    db = get_user_database()
    
    # Tabs para diferentes ações
    tab1, tab2, tab3 = st.tabs(["📋 Listar Usuários", "➕ Adicionar Usuário", "🔑 Alterar Senha"])
    
    # =====================================================================
    # TAB 1: LISTAR USUÁRIOS
    # =====================================================================
    with tab1:
        st.subheader("📋 Usuários Cadastrados")
        
        users = db.list_users()
        
        if not users:
            st.info("Nenhum usuário cadastrado.")
        else:
            for user in users:
                col1, col2, col3, col4, col5 = st.columns([2, 2, 1, 1, 1])
                
                with col1:
                    status_icon = "✅" if user['active'] else "🚫"
                    st.write(f"{status_icon} **{user['username']}**")
                
                with col2:
                    st.write(user['full_name'])
                
                with col3:
                    role_badge = "🔴 Admin" if user['role'] == 'admin' else "🔵 User"
                    st.write(role_badge)
                
                with col4:
                    # Botão para desativar/ativar
                    if user['username'] != st.session_state.user['username']:  # Não pode desativar a si mesmo
                        if user['active']:
                            if st.button("🚫 Desativar", key=f"deactivate_{user['id']}"):
                                if db.update_user(user['username'], active=False):
                                    st.success(f"✅ Usuário {user['username']} desativado!")
                                    st.rerun()
                        else:
                            if st.button("✅ Ativar", key=f"activate_{user['id']}"):
                                if db.update_user(user['username'], active=True):
                                    st.success(f"✅ Usuário {user['username']} ativado!")
                                    st.rerun()
                
                with col5:
                    # Expander para editar
                    with st.expander("✏️"):
                        new_name = st.text_input("Nome completo", value=user['full_name'], key=f"name_{user['id']}")
                        new_role = st.selectbox("Papel", ['user', 'admin'], 
                                               index=0 if user['role'] == 'user' else 1,
                                               key=f"role_{user['id']}")
                        
                        if st.button("💾 Salvar", key=f"save_{user['id']}"):
                            if db.update_user(user['username'], full_name=new_name, role=new_role):
                                st.success("✅ Usuário atualizado!")
                                st.rerun()
                
                st.markdown("---")
    
    # =====================================================================
    # TAB 2: ADICIONAR USUÁRIO
    # =====================================================================
    with tab2:
        st.subheader("➕ Adicionar Novo Usuário")
        
        with st.form("add_user_form"):
            new_username = st.text_input("👤 Nome de usuário", help="Único, sem espaços")
            new_password = st.text_input("🔑 Senha", type="password")
            new_password_confirm = st.text_input("🔑 Confirmar senha", type="password")
            new_full_name = st.text_input("📝 Nome completo")
            new_role = st.selectbox("🎭 Papel", ['user', 'admin'])
            
            submit = st.form_submit_button("➕ Criar Usuário")
            
            if submit:
                # Validações
                if not new_username or not new_password or not new_full_name:
                    st.error("❌ Preencha todos os campos!")
                elif ' ' in new_username:
                    st.error("❌ Nome de usuário não pode conter espaços!")
                elif len(new_password) < 6:
                    st.error("❌ Senha deve ter pelo menos 6 caracteres!")
                elif new_password != new_password_confirm:
                    st.error("❌ Senhas não coincidem!")
                elif db.get_user(new_username):
                    st.error(f"❌ Usuário '{new_username}' já existe!")
                else:
                    # Criar usuário
                    if db.create_user(new_username, new_password, new_full_name, new_role):
                        st.success(f"✅ Usuário '{new_username}' criado com sucesso!")
                        st.balloons()
                        st.rerun()
    
    # =====================================================================
    # TAB 3: ALTERAR SENHA
    # =====================================================================
    with tab3:
        st.subheader("🔑 Alterar Senha de Usuário")
        
        users_list = db.list_users()
        usernames = [u['username'] for u in users_list if u['active']]
        
        if not usernames:
            st.info("Nenhum usuário ativo.")
        else:
            with st.form("change_password_form"):
                selected_user = st.selectbox("👤 Selecionar usuário", usernames)
                new_pwd = st.text_input("🔑 Nova senha", type="password")
                new_pwd_confirm = st.text_input("🔑 Confirmar nova senha", type="password")
                
                submit = st.form_submit_button("💾 Alterar Senha")
                
                if submit:
                    if not new_pwd:
                        st.error("❌ Digite a nova senha!")
                    elif len(new_pwd) < 6:
                        st.error("❌ Senha deve ter pelo menos 6 caracteres!")
                    elif new_pwd != new_pwd_confirm:
                        st.error("❌ Senhas não coincidem!")
                    else:
                        if db.change_password(selected_user, new_pwd):
                            st.success(f"✅ Senha de '{selected_user}' alterada com sucesso!")
                        else:
                            st.error("❌ Erro ao alterar senha!")
