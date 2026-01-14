# 🚀 Deploy no Streamlit Cloud - Guia Completo

## 📋 Pré-requisitos

- Código no GitHub
- Conta no [Streamlit Cloud](https://share.streamlit.io)
- Credenciais do Google (arquivo `google_credentials.json`)

---

## 🔐 Configurar Secrets no Streamlit Cloud

### 1. Copiar Conteúdo do JSON

Abra `google_credentials.json` e copie **TODO** o conteúdo.

### 2. Acessar Configurações do App

1. Vá em [share.streamlit.io](https://share.streamlit.io)
2. Selecione seu app (ou faça deploy primeiro)
3. Clique em **⚙️ Settings** → **Secrets**

### 3. Adicionar Secrets

Cole o seguinte no editor de secrets (substitua os valores pelos do seu `google_credentials.json`):

```toml
# =====================================================================
# AUTENTICAÇÃO - Admin
# =====================================================================
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD_HASH = "$2b$12$/UE9jxxnHz.dW86iF1/feeOefidtkIm7ghARwwbD1x4R4W.sIwiHW"
ADMIN_NAME = "Administrador CRECI"

# =====================================================================
# GOOGLE SHEETS - URLs
# =====================================================================
GOOGLE_SHEET_CORRETORES = "https://docs.google.com/spreadsheets/d/SEU_ID_AQUI/edit"
GOOGLE_SHEET_IMOBILIARIAS = "https://docs.google.com/spreadsheets/d/SEU_ID_AQUI/edit"

# =====================================================================
# GOOGLE SHEETS - Credenciais (Service Account)
# =====================================================================
[gcp_service_account]
type = "service_account"
project_id = "gen-lang-client-0616780260"
private_key_id = "ad91bb515f93e1afd7d44b87abcf4b578828ab06"
private_key = "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDELuGiI9CHLcmV\n71x238oi4GVSHFF8q9WBGcKgxuzgwD4JpNUZwLNMTUSV6udSQ6CwGDUY+j1ooQ21\nnuHvMUvE3kSECLwSPrwoovUOGHzlfyVszK3vdhCe3wfbf4d40ZBVgJso2Qwwic0D\nMXrWNIKR4+TxK5cvzIo4h6N2+Cl5E4o3atwwxcedbMcHleIvMluo4u2ORHYiiPU9\nYxvzJGnrLCdA+AeRUbKfgyjBXkmGqfJ8M551ymUEIu8mqIMZN3z32i9V1EdWUu0c\niNs+lEPNyo+F9/309gNscT04/uvxY/6byy4b4Wvr3vgqtM1a1qlQ2IHnWJEb+uuw\n2SFofIUZAgMBAAECggEASr4Tv6rGcSH8Kc/6Wd3UDKqSX5CjaQyseJWgZZG0QMJt\nQE5Y1AlrJhhQF4/Z1qkmSMDIRf5ctAacCwR/zpno5JXL48PSJ19YX2EKXPbuap8g\n2o02fUNtfKG7RCCXs+ufgjvPoWXj84Akp+FLi92Qm1WIbWuum4rhZD0lBZfxcQta\nVusyj2/ADGOMXqXvulOPZeTKHUg9DscOAGp2TuJF9rUHvxfQIcQxhSR5/RGeYDWA\nXXlB7DGBudQ8rp8sMI/OSQNftSVhV3anwhi91lgCC9Y1taLYcsTUsBpbGwOAL+vW\n15XukkXlF9H8WbbxtVn7fWr4k5ZLOOsZbZqsuCq9ewKBgQDpeEvfck04S4cL8jQK\nM4iTiy6zoeEcs5ILPBsSPvD90xXmODOR9/YZghI+zCUTB4JVODjp8/nwMgiPFgQo\nhIvm7zvgVWT06BOToygfIqDsTvvItSOY9NOyn1MmlO67Nf2+WZpfdAESDKECg/E9\nb0yTbAFQIGCG5A2KDCrxeIhTtwKBgQDXHXFAdUMMzdAr37XNDP4pMj5qPqIlHiZc\nmihtBTf18d02YATm22tNecylOhybmO09EqqpYMe0z5TI5G2DTY0KAEvopDgdgwZo\nW9l2rkBD8yJ8cVFq8i/tRD7pOMaOlTo/dvhJUyBHhbE1/IbMjtSe6OlSWFNrxybx\nYHoZX00NrwKBgQCDGMmB7uztb3uleZs/HzDRqJXQyFVfiHW5WUbaN/2aia0CWQyc\nKmBGcoNMP9WRmeXVdHyA4j62YWHs9q/fEI5+XleA4HKQEsDrZfJhiVBTYQaA7TXP\n7anx4wUN5RMojGivOiE0+C6hs/W1M+GCXbziCwOxunx5QhVYLvzuGoBygQKBgDlJ\naPiegc2uHcshV3wVArab381RgsLZxaORlkR6SE3iLGQnrAaC1o+aaSpzUF0Lm9pQ\n10wmLujzAw+A7b0y8OWB8LUyzpLlatZt53rYqtqtrDhxwRn3B1Zrf0mCyjX8fbeb\nCkIUthr1+pyC9K8TNoJfSouYZBbmwXM0my+Ylp+XAoGBAK/Wcl/avBrc8dj88IB6\nMEUxsk3EOvsITf5z4svh0Mu1Szbi7KEuXIp9SDB4Yd+MQQK0K7oQkT/1t6AzY2mO\nO9FMAeWtkpwiRy7atPfUGktDyWYEul71vHP1ZwqB7njvhR9tUYN8M20tFgmRFXai\n9fo5aXTm/c7TS6rfeTBh1s9c\n-----END PRIVATE KEY-----\n"
client_email = "creci-sheets-reader@gen-lang-client-0616780260.iam.gserviceaccount.com"
client_id = "117284419519492236178"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "https://www.googleapis.com/robot/v1/metadata/x509/creci-sheets-reader%40gen-lang-client-0616780260.iam.gserviceaccount.com"
universe_domain = "googleapis.com"

# =====================================================================
# CONFIGURAÇÕES OPCIONAIS
# =====================================================================
SHEET_NAME_CORRETORES = "Corretores"
SHEET_NAME_IMOBILIARIAS = "Imobiliárias"
```

### 4. Salvar

Clique em **Save** no canto inferior direito.

---

## 🚀 Deploy do App

### Novo Deploy

1. Acesse [share.streamlit.io](https://share.streamlit.io)
2. Clique em **New app**
3. Preencha:
   - **Repository**: `seu-usuario/Creci_Itinerante`
   - **Branch**: `main`
   - **Main file path**: `app.py`
4. Clique em **Deploy!**

### Atualizar Deploy Existente

O app é atualizado automaticamente quando você faz push no GitHub.

Para forçar atualização:
1. Vá nas configurações do app
2. Clique em **Reboot app**

---

## ✅ Verificação

Após deploy, teste:
1. Acesse a URL do seu app
2. Faça login com as credenciais configuradas
3. Verifique se os dados do Google Sheets carregam corretamente

---

## 🔒 Segurança

### Checklist de Segurança

- ✅ `google_credentials.json` **NÃO** está no GitHub
- ✅ `.env` **NÃO** está no GitHub
- ✅ Secrets configurados no Streamlit Cloud
- ✅ Planilhas compartilhadas apenas com Service Account
- ✅ Service Account tem apenas permissão de **Viewer**

### Variáveis de Ambiente vs Secrets

**Streamlit Cloud usa st.secrets**, não variáveis de ambiente normais. O código já está preparado para:
1. Tentar `st.secrets` primeiro (Cloud)
2. Se falhar, tentar arquivo local (desenvolvimento)

---

## 🛠️ Solução de Problemas

### Erro: "Credenciais não encontradas"
- Verifique se configurou os secrets corretamente
- Certifique-se que a seção `[gcp_service_account]` existe

### Erro: "Permission denied"
- Verifique se compartilhou as planilhas com o email da Service Account
- Email: `creci-sheets-reader@gen-lang-client-0616780260.iam.gserviceaccount.com`

### Erro de Autenticação
- Verifique se o `ADMIN_PASSWORD_HASH` está correto nos secrets
- Use a senha `1!EaSmtaK` para fazer login

### App não inicia
- Veja os logs no Streamlit Cloud
- Verifique se todas as dependências estão em `requirements.txt`

---

## 📝 Comandos Git para Deploy

```powershell
# Fazer commit das mudanças
git add .
git commit -m "Preparado para deploy no Streamlit Cloud"

# Enviar para GitHub
git push origin main
```

O Streamlit Cloud detecta automaticamente e faz redeploy.

---

**Pronto para produção! 🎉**
