import time

import pymongo
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from pymongo.server_api import ServerApi

from src.utils.config import Config


class DatabaseManager:
    def __init__(self, database_name=None):
        self.database_name = database_name or Config.DATABASE_NAME
        self.client = None
        self.db = None
        self._connect()
    
    def _connect(self, retries=3, delay=2):
        """Estabelece conexão com o MongoDB Atlas com tentativas de retry"""
        for attempt in range(retries):
            try:
                print(f"Tentativa {attempt + 1} de conexão com MongoDB Atlas...")
                print(f"URI: {Config.MONGODB_URI[:50]}...")  # Mostrar apenas parte da URI por segurança
                
                # Conexão para MongoDB Atlas com Server API
                self.client = MongoClient(
                    Config.MONGODB_URI,
                    server_api=ServerApi('1'),
                    serverSelectionTimeoutMS=10000,
                    connectTimeoutMS=15000,
                    socketTimeoutMS=15000,
                    retryWrites=True,
                    w='majority'
                )
                
                # Testar a conexão com ping
                self.client.admin.command('ping')
                self.db = self.client[self.database_name]
                
                print(f"✓ Conectado ao MongoDB Atlas com sucesso!")
                print(f"✓ Banco de dados: {self.database_name}")
                return
                
            except ServerSelectionTimeoutError as e:
                print(f"✗ Timeout na tentativa {attempt + 1}: {e}")
                if attempt < retries - 1:
                    print(f" Aguardando {delay} segundos antes da próxima tentativa...")
                    time.sleep(delay)
                else:
                    raise ConnectionFailure(f"Falha ao conectar com MongoDB Atlas após {retries} tentativas: {e}")
            
            except ConnectionFailure as e:
                print(f"✗ Falha de conexão na tentativa {attempt + 1}: {e}")
                if attempt < retries - 1:
                    print(f" Aguardando {delay} segundos antes da próxima tentativa...")
                    time.sleep(delay)
                else:
                    raise
            
            except Exception as e:
                print(f"✗ Erro inesperado na tentativa {attempt + 1}: {e}")
                if attempt < retries - 1:
                    print(f" Aguardando {delay} segundos antes da próxima tentativa...")
                    time.sleep(delay)
                else:
                    raise
    
    def get_collection(self, collection_name):
        """Retorna uma coleção do MongoDB"""
        if self.db is None:
            self._connect()
        return self.db[collection_name]
    
    def create_indexes(self):
        """Cria índices para melhor performance"""
        try:
            collection = self.get_collection('matches')
            
            # Índices para consultas comuns
            indexes = [
                [('year', 1)],
                [('tournament_id', 1)],
                [('match_id', 1)],  # Único
                [('stage_name', 1)],
                [('team_a.name', 1)],
                [('team_b.name', 1)],
                [('winner', 1)],
                [('match_date', 1)]
            ]
            
            for index in indexes:
                collection.create_index(index)
            
            # Índice único para match_id
            collection.create_index([('match_id', 1)], unique=True, sparse=True)
            
            print("✓ Índices criados com sucesso!")
            
        except Exception as e:
            print(f"✗ Erro ao criar índices: {e}")
    
    def test_connection(self):
        """Testa se a conexão está ativa"""
        try:
            self.client.admin.command('ping')
            return True
        except:
            return False
    
    def get_database_info(self):
        """Retorna informações sobre o banco de dados"""
        try:
            if self.db is None:
                return "Não conectado"
            
            collections = self.db.list_collection_names()
            stats = self.db.command('dbStats')
            
            info = {
                'database_name': self.database_name,
                'collections': collections,
                'collections_count': len(collections),
                'total_size': stats.get('dataSize', 0),
                'storage_size': stats.get('storageSize', 0)
            }
            
            return info
            
        except Exception as e:
            return f"Erro ao obter informações: {e}"
    
    def close_connection(self):
        """Fecha a conexão com o MongoDB"""
        if self.client:
            self.client.close()
            print("✓ Conexão com MongoDB Atlas fechada.")

# Função auxiliar para verificar a conexão
def test_mongodb_connection():
    """Testa a conexão com o MongoDB Atlas"""
    return Config.test_connection()

# Exemplo de uso seguro
if __name__ == "__main__":
    # Testar conexão
    if test_mongodb_connection():
        try:
            db = DatabaseManager()
            print("✓ DatabaseManager inicializado com sucesso!")
            print(f"✓ Informações do banco: {db.get_database_info()}")
            db.close_connection()
        except Exception as e:
            print(f"✗ Erro no DatabaseManager: {e}")
    else:
        print("✗ Não foi possível conectar ao MongoDB Atlas")