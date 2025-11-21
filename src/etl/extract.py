import numpy as np
import pandas as pd


class DataExtractor:
    def __init__(self):
        pass
    
    def load_worldcup_data(self, file_path):
        """Carrega dados específicos da Copa do Mundo"""
        try:
            df = pd.read_csv(file_path, encoding='utf-8')
            print(f"Dataset carregado: {len(df)} partidas de {df['year'].min()} a {df['year'].max()}")
            return df
        except UnicodeDecodeError:
            # Tentar com encoding diferente se necessário
            df = pd.read_csv(file_path, encoding='latin-1')
            print(f"Dataset carregado (latin-1): {len(df)} partidas")
            return df
        except Exception as e:
            print(f"Erro ao carregar arquivo: {e}")
            return None
    
    def analyze_dataset(self, df):
        """Analisa estrutura do dataset"""
        print("\n=== ANÁLISE DO DATASET ===")
        print(f"Período: {df['year'].min()} - {df['year'].max()}")
        print(f"Total de Copas: {df['year'].nunique()}")
        print(f"Total de Partidas: {len(df)}")
        print(f"Colunas disponíveis: {list(df.columns)}")
        
        # Estatísticas básicas
        print(f"\nFases da competição: {df['stage_name'].unique()}")
        print(f"Países participantes: {pd.concat([df['team_a_name'], df['team_b_name']]).nunique()}")
        
        return df.info()