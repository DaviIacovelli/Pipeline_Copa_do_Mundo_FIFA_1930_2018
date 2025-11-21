class ColumnMapper:
    """Mapeia colunas do dataset para nomes padronizados"""
    
    @classmethod
    def get_column_mapping(cls, df):
        """Retorna o mapeamento de colunas baseado na estrutura real"""
        mapping = {
            # Colunas principais baseadas na sua estrutura
            'team_a_col': 'team_a_name',
            'team_b_col': 'team_b_name',
            'team_a_score_col': 'team_a_score',
            'team_b_score_col': 'team_b_score',
            'stage_col': 'stage_name',
            'tournament_col': 'tournament_id',
            'year_col': 'year',
            'match_id_col': 'match_id',
            'group_col': 'group_name',
            'stadium_col': 'stadium_name',
            'city_col': 'city_name',
            'country_col': 'country_name',
            'date_col': 'match_date',
            'time_col': 'match_time',
            
            # Colunas booleanas de resultado
            'team_a_win_col': 'team_a_win',
            'team_b_win_col': 'team_b_win', 
            'draw_col': 'draw',
            'extra_time_col': 'extra_time',
            'penalty_shootout_col': 'penalty_shootout',
            
            # Colunas de pênaltis
            'penalties_score_col': 'score_penalties',
            'team_a_penalties_col': 'team_a_score_penalties',
            'team_b_penalties_col': 'team_b_score_penalties'
        }
        
        # Verificar se as colunas essenciais existem
        essential_cols = ['team_a_col', 'team_b_col', 'team_a_score_col', 'team_b_score_col']
        for col in essential_cols:
            if mapping[col] not in df.columns:
                print(f"⚠️  Coluna essencial não encontrada: {mapping[col]}")
        
        return mapping