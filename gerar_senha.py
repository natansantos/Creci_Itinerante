# 🔐 Script Auxiliar - Gerador de Hash de Senha
# Use este script para gerar hashes de senhas para o arquivo .env

import bcrypt
import sys

def gerar_hash_senha(senha):
    """
    Gera um hash bcrypt para uma senha.
    
    Args:
        senha: Senha em texto plano
    
    Returns:
        Hash da senha
    """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(senha.encode('utf-8'), salt)
    return hashed.decode('utf-8')


if __name__ == "__main__":
    print("=" * 60)
    print("🔐 GERADOR DE HASH DE SENHA - CRECI Itinerante")
    print("=" * 60)
    print()
    
    if len(sys.argv) > 1:
        # Senha passada como argumento
        senha = sys.argv[1]
    else:
        # Solicitar senha interativamente
        senha = input("Digite a senha que deseja usar para login: ")
    
    if not senha:
        print("❌ Senha não pode ser vazia!")
        sys.exit(1)
    
    if len(senha) < 6:
        print("⚠️  Aviso: Senha muito curta! Recomendamos pelo menos 8 caracteres.")
    
    print()
    print("⏳ Gerando hash...")
    hash_gerado = gerar_hash_senha(senha)
    
    print()
    print("✅ Hash gerado com sucesso!")
    print()
    print("=" * 60)
    print("COPIE O HASH ABAIXO PARA O ARQUIVO .env:")
    print("=" * 60)
    print()
    print(hash_gerado)
    print()
    print("=" * 60)
    print()
    print("📝 Instruções:")
    print("1. Abra o arquivo .env")
    print("2. Localize a linha: ADMIN_PASSWORD_HASH=...")
    print("3. Substitua pelo hash gerado acima")
    print("4. Salve o arquivo")
    print()
    print("⚠️  IMPORTANTE: Guarde a senha original em local seguro!")
    print("   O hash acima NÃO pode ser usado para fazer login.")
    print("   Use a senha ORIGINAL que você digitou.")
    print()
