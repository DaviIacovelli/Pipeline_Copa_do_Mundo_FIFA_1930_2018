import os
from datetime import datetime
from urllib.parse import quote_plus

from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configurações globais do projeto"""
    
    # MongoDB - Usar a URI diretamente do .env
    MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
    DATABASE_NAME = os.getenv('MONGODB_DB_NAME', 'fifa_worldcup_analysis')
    
    # Paths
    DATA_RAW_PATH = 'data/raw/'
    DATA_PROCESSED_PATH = 'data/processed/'
    DATABASE_BACKUP_PATH = 'data/database/'
    DOCS_PATH = 'docs/'
    IMAGES_PATH = 'docs/imagens/'
    
    # Analysis Settings
    TOP_TEAMS_LIMIT = 10
    MIN_MATCHES_FOR_ANALYSIS = 5
    START_YEAR = 1930
    END_YEAR = 2022
    
    # Visualization Settings
    CHART_WIDTH = 1200
    CHART_HEIGHT = 600
    COLOR_PALETTE = [
        '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
        '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf'
    ]
    
    # Export Settings
    EXPORT_HTML = True
    EXPORT_PNG = True
    EXPORT_JSON = True
    
    @classmethod
    def create_directories(cls):
        """Cria todos os diretórios necessários"""
        directories = [
            cls.DATA_RAW_PATH,
            cls.DATA_PROCESSED_PATH,
            cls.DATABASE_BACKUP_PATH,
            cls.IMAGES_PATH,
            'logs/',
            'temp/'
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
        print("✓ Diretórios criados com sucesso!")

    @classmethod
    def get_current_timestamp(cls):
        """Retorna timestamp atual para uso em arquivos"""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @classmethod
    def test_connection(cls):
        """Testa a conexão com o MongoDB"""
        try:
            from pymongo import MongoClient
            from pymongo.server_api import ServerApi
            
            client = MongoClient(cls.MONGODB_URI, server_api=ServerApi('1'))
            client.admin.command('ping')
            print("✓ Conexão com MongoDB estabelecida com sucesso!")
            client.close()
            return True
        except Exception as e:
            print(f"✗ Erro na conexão com MongoDB: {e}")
            return False