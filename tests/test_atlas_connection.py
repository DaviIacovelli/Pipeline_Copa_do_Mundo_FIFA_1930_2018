#!/usr/bin/env python3
"""
Script específico para testar conexão com MongoDB Atlas
"""

import os
import sys

from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

def test_atlas_connection():
    """Testa a conexão direta com MongoDB Atlas"""
    try:
        from pymongo.mongo_client import MongoClient
        from pymongo.server_api import ServerApi

        # Obter URI do .env
        uri = os.getenv('MONGODB_URI')
        if not uri:
            print("✗ MONGODB_URI não encontrada no arquivo .env")
            return False
        
        print("=== TESTE DE CONEXÃO MONGODB ATLAS ===")
        print(f"URI: {uri[:50]}...")  # Mostrar apenas parte por segurança
        
        # Criar cliente e conectar
        client = MongoClient(uri, server_api=ServerApi('1'))
        
        # Enviar ping para confirmar conexão
        client.admin.command('ping')
        print("✅ Ping realizado com sucesso! Conexão estabelecida.")
        
        # Listar bancos de dados disponíveis
        databases = client.list_database_names()
        print(f"📊 Bancos de dados disponíveis: {databases}")
        
        client.close()
        return True
        
    except Exception as e:
        print(f"❌ Erro na conexão: {e}")
        return False

def main():
    """Função principal"""
    print("Iniciando teste de conexão com MongoDB Atlas...\n")
    
    if test_atlas_connection():
        print("\n🎉 Conexão com MongoDB Atlas bem-sucedida!")
        print("\nPróximos passos:")
        print("1. Execute: python main.py")
        print("2. Verifique se os dados foram carregados")
        return True
    else:
        print("\n💡 Solução de problemas:")
        print("1. Verifique se a senha no .env está correta")
        print("2. Verifique se o IP está na whitelist do Atlas")
        print("3. Verifique a conexão com internet")
        print("4. Execute: python -m pip install \"pymongo[srv]\"")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)