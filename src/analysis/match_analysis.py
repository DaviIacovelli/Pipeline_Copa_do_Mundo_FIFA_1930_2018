from src.database.db import DatabaseManager


class MatchAnalyzer:
    def __init__(self):
        self.db_manager = DatabaseManager()
    
    def get_high_scoring_matches(self, min_goals=7, limit=10):
        """Partidas com maior número de gols"""
        pipeline = [
            {
                '$match': {
                    'total_goals': {'$gte': min_goals}
                }
            },
            {
                '$project': {
                    'year': 1,
                    'stage_name_std': 1,
                    'team_a_name': 1,
                    'team_b_name': 1,
                    'team_a_score': 1,
                    'team_b_score': 1,
                    'total_goals': 1,
                    'result': 1,
                    'venue': 1
                }
            },
            {'$sort': {'total_goals': -1}},
            {'$limit': limit}
        ]
        
        collection = self.db_manager.get_collection('matches')
        return list(collection.aggregate(pipeline))
    
    def analyze_final_matches(self):
        """Análise específica das finais"""
        pipeline = [
            {
                '$match': {
                    'stage_name_std': 'Final'
                }
            },
            {
                '$project': {
                    'year': 1,
                    'champion': {
                        '$cond': [
                            {'$eq': ['$winner', '$team_a_name']},
                            '$team_a_name',
                            '$team_b_name'
                        ]
                    },
                    'runner_up': {
                        '$cond': [
                            {'$eq': ['$winner', '$team_a_name']},
                            '$team_b_name',
                            '$team_a_name'
                        ]
                    },
                    'score': {
                        '$concat': [
                            {'$toString': '$team_a_score'},
                            '-',
                            {'$toString': '$team_b_score'}
                        ]
                    },
                    'total_goals': 1,
                    'extra_time': 1,
                    'penalty_shootout': 1,
                    'venue': 1,
                    'win_type': 1
                }
            },
            {'$sort': {'year': 1}}
        ]
        
        collection = self.db_manager.get_collection('matches')
        return list(collection.aggregate(pipeline))
    
    def get_head_to_head(self, team1, team2):
        """Histórico de confrontos entre duas seleções"""
        pipeline = [
            {
                '$match': {
                    '$or': [
                        {
                            'team_a_name': team1,
                            'team_b_name': team2
                        },
                        {
                            'team_a_name': team2,
                            'team_b_name': team1
                        }
                    ]
                }
            },
            {
                '$project': {
                    'year': 1,
                    'stage_name_std': 1,
                    'team1': team1,
                    'team2': team2,
                    'team1_goals': {
                        '$cond': [
                            {'$eq': ['$team_a_name', team1]},
                            '$team_a_score',
                            '$team_b_score'
                        ]
                    },
                    'team2_goals': {
                        '$cond': [
                            {'$eq': ['$team_a_name', team1]},
                            '$team_b_score',
                            '$team_a_score'
                        ]
                    },
                    'winner': 1,
                    'venue': 1,
                    'win_type': 1
                }
            },
            {'$sort': {'year': 1}}
        ]
        
        collection = self.db_manager.get_collection('matches')
        matches = list(collection.aggregate(pipeline))
        
        # Calcular estatísticas do confronto
        if matches:
            stats = {
                'total_matches': len(matches),
                'team1_wins': sum(1 for m in matches if m['winner'] == team1),
                'team2_wins': sum(1 for m in matches if m['winner'] == team2),
                'draws': sum(1 for m in matches if m['winner'] == 'Draw'),
                'team1_goals': sum(m['team1_goals'] for m in matches),
                'team2_goals': sum(m['team2_goals'] for m in matches),
                'matches': matches
            }
            return stats
        return None