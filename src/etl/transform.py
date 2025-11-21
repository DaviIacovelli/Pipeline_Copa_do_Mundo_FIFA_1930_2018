from datetime import datetime

import numpy as np
import pandas as pd

from .column_mapper import ColumnMapper


class DataTransformer:
    def __init__(self):
        self.column_mapping = None
    
    def analyze_and_map_columns(self, df):
        """Analisa e mapeia as colunas do dataset"""
        self.column_mapping = ColumnMapper.get_column_mapping(df)
        
        print("=== MAPEAMENTO DE COLUNAS ===")
        for key, value in self.column_mapping.items():
            if value in df.columns:
                print(f"  ✅ {key}: {value}")
            else:
                print(f"  ❌ {key}: {value} (não encontrada)")
        
        return self.column_mapping
    
    def clean_worldcup_data(self, df):
        """Limpa e transforma dados da Copa do Mundo"""
        df_clean = df.copy()
        
        print("Iniciando transformação dos dados...")
        
        # 1. Analisar e mapear colunas
        self.analyze_and_map_columns(df_clean)
        
        # 2. Converter tipos de dados
        df_clean = self._convert_data_types(df_clean)
        
        # 3. Tratar valores nulos
        df_clean = self._handle_missing_values(df_clean)
        
        # 4. Adicionar colunas derivadas
        df_clean = self._create_derived_columns(df_clean)
        
        # 5. Padronizar nomes
        df_clean = self._standardize_data(df_clean)
        
        print("✅ Transformação concluída!")
        return df_clean
    
    def _convert_data_types(self, df):
        """Converte tipos de dados baseado no mapeamento"""
        # Datas
        if 'match_date' in df.columns:
            df['match_date'] = pd.to_datetime(df['match_date'], errors='coerce')
        
        # Colunas numéricas
        numeric_columns = [
            'year', 'team_a_score', 'team_b_score', 
            'team_a_score_margin', 'team_b_score_margin',
            'team_a_score_penalties', 'team_b_score_penalties'
        ]
        
        for col in numeric_columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        
        # Colunas booleanas
        bool_columns = [
            'replayed', 'replay', 'extra_time', 'penalty_shootout',
            'team_a_win', 'team_b_win', 'draw'
        ]
        
        for col in bool_columns:
            if col in df.columns:
                df[col] = df[col].fillna(0).astype(bool)
        
        return df
    
    def _handle_missing_values(self, df):
        """Trata valores missing"""
        # Preencher scores missing com 0
        score_cols = ['team_a_score', 'team_b_score']
        for col in score_cols:
            if col in df.columns:
                df[col] = df[col].fillna(0)
        
        # Preencher nomes de times missing
        team_cols = ['team_a_name', 'team_b_name']
        for col in team_cols:
            if col in df.columns:
                df[col] = df[col].fillna('Unknown')
        
        # Preencher estádios e cidades
        location_cols = ['stadium_name', 'city_name', 'country_name']
        for col in location_cols:
            if col in df.columns:
                df[col] = df[col].fillna('Unknown')
        
        # Preencher group_name para fases eliminatórias
        if 'group_name' in df.columns:
            df['group_name'] = df['group_name'].fillna('Knockout Stage')
        
        return df
    
    def _create_derived_columns(self, df):
        """Cria colunas derivadas para análise"""
        # Total de gols
        df['total_goals'] = df['team_a_score'] + df['team_b_score']
        
        # Diferença de gols
        df['goal_difference'] = abs(df['team_a_score'] - df['team_b_score'])
        
        # Resultado formatado
        df['result'] = df.apply(
            lambda row: f"{row['team_a_name']} {row['team_a_score']}-{row['team_b_score']} {row['team_b_name']}", 
            axis=1
        )
        
        # Identificador do vencedor baseado nas colunas booleanas
        df['winner'] = df.apply(self._get_winner_from_booleans, axis=1)
        
        # Tipo de vitória
        df['win_type'] = df.apply(self._determine_win_type, axis=1)
        
        # Informações completas do estádio
        if 'stadium_name' in df.columns and 'city_name' in df.columns:
            df['venue'] = df['stadium_name'] + ', ' + df['city_name']
        
        # Classificar importância da fase
        df['stage_importance'] = df['stage_name'].apply(self._classify_stage_importance)
        
        return df
    
    def _get_winner_from_booleans(self, row):
        """Identifica o vencedor usando as colunas booleanas"""
        try:
            if row['team_a_win']:
                return row['team_a_name']
            elif row['team_b_win']:
                return row['team_b_name']
            elif row['draw']:
                return 'Draw'
            else:
                # Fallback: determinar pelo placar
                if row['team_a_score'] > row['team_b_score']:
                    return row['team_a_name']
                elif row['team_b_score'] > row['team_a_score']:
                    return row['team_b_name']
                else:
                    return 'Draw'
        except:
            return 'Unknown'
    
    def _determine_win_type(self, row):
        """Determina o tipo de vitória"""
        if row['draw']:
            return 'Draw'
        elif row['penalty_shootout']:
            return 'Penalties'
        elif row['extra_time']:
            return 'Extra Time'
        else:
            return 'Regular Time'
    
    def _classify_stage_importance(self, stage_name):
        """Classifica a importância da fase"""
        important_stages = ['final', 'semi-final', 'third-place match']
        group_stages = ['group stage', 'first stage', 'second stage']
        
        stage_lower = str(stage_name).lower()
        
        if any(important in stage_lower for important in important_stages):
            return 'High'
        elif any(group in stage_lower for group in group_stages):
            return 'Medium'
        else:
            return 'Low'
    
    def _standardize_data(self, df):
        """Padroniza nomes e categorias"""
        # Padronizar nomes de estágios
        if 'stage_name' in df.columns:
            stage_mapping = {
                'final': 'Final',
                'semi-final': 'Semi-Final',
                'third-place match': 'Third Place',
                'quarter-final': 'Quarter-Final',
                'round of 16': 'Round of 16',
                'group stage': 'Group Stage',
                'first stage': 'First Stage',
                'second stage': 'Second Stage'
            }
            df['stage_name_std'] = df['stage_name'].replace(stage_mapping)
        
        # Padronizar nomes de países (exemplo: corrigir nomes históricos)
        country_mapping = {
            'West Germany': 'Germany',
            'West Germany FR': 'Germany', 
            'Soviet Union': 'Russia',
            'Czechoslovakia': 'Czech Republic',
            'Yugoslavia': 'Serbia'
        }
        
        for team_col in ['team_a_name', 'team_b_name']:
            if team_col in df.columns:
                df[team_col] = df[team_col].replace(country_mapping)
        
        return df