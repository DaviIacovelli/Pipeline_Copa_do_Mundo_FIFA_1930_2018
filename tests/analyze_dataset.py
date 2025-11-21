import os

import pandas as pd


def analyze_csv_structure():
    """Analisa a estrutura real do arquivo CSV"""
    file_path = 'data/raw/world_fifa_worldcup_matches.csv'
    
    if not os.path.exists(file_path):
        print(f"❌ Arquivo não encontrado: {file_path}")
        return None
    
    try:
        # Ler o arquivo
        df = pd.read_csv(file_path, encoding='utf-8')
        
        print("=== ESTRUTURA DO DATASET ===")
        print(f"📊 Total de linhas: {len(df)}")
        print(f"📋 Total de colunas: {len(df.columns)}")
        print(f"🎯 Colunas disponíveis:")
        
        for i, col in enumerate(df.columns):
            print(f"  {i+1:2d}. '{col}'")
        
        print(f"\n📅 Período: {df['year'].min()} - {df['year'].max()}")
        print(f"🏆 Edições: {df['year'].nunique()}")
        
        # Mostrar algumas linhas para ver a estrutura
        print(f"\n🔍 Primeiras 3 linhas:")
        print(df.head(3).to_string())
        
        # Verificar colunas relacionadas a times
        team_columns = [col for col in df.columns if 'team' in col.lower()]
        print(f"\n⚽ Colunas relacionadas a times: {team_columns}")
        
        # Verificar colunas de score
        score_columns = [col for col in df.columns if 'score' in col.lower()]
        print(f"📈 Colunas relacionadas a placar: {score_columns}")
        
        return df.columns.tolist()
        
    except Exception as e:
        print(f"❌ Erro ao analisar o arquivo: {e}")
        return None

if __name__ == "__main__":
    analyze_csv_structure()