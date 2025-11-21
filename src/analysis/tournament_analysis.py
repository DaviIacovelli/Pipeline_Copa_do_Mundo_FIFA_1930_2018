import pandas as pd

from src.database.db import DatabaseManager


class TournamentAnalyzer:
    def __init__(self):
        self.db_manager = DatabaseManager()
    
    def get_tournament_summary(self):
        """Resumo geral de todas as Copas"""
        pipeline = [
            {
                '$group': {
                    '_id': '$year',
                    'edition': {'$first': '$tournament_id'},
                    'total_matches': {'$sum': 1},
                    'total_goals': {'$sum': '$total_goals'},
                    'avg_goals_per_match': {'$avg': '$total_goals'},
                    'matches_with_extra_time': {'$sum': {'$cond': ['$extra_time', 1, 0]}},
                    'matches_with_penalties': {'$sum': {'$cond': ['$penalty_shootout', 1, 0]}},
                    'total_draws': {'$sum': {'$cond': ['$draw', 1, 0]}}
                }
            },
            {'$sort': {'_id': 1}}
        ]
        
        collection = self.db_manager.get_collection('matches')
        results = list(collection.aggregate(pipeline))
        return results
    
    def get_team_performance(self, team_name):
        """Desempenho histórico de uma seleção"""
        pipeline = [
            {
                '$match': {
                    '$or': [
                        {'team_a_name': team_name},
                        {'team_b_name': team_name}
                    ]
                }
            },
            {
                '$project': {
                    'year': 1,
                    'stage_name': 1,
                    'team': team_name,
                    'is_home': {'$eq': ['$team_a_name', team_name]},
                    'goals_scored': {
                        '$cond': [
                            {'$eq': ['$team_a_name', team_name]},
                            '$team_a_score',
                            '$team_b_score'
                        ]
                    },
                    'goals_conceded': {
                        '$cond': [
                            {'$eq': ['$team_a_name', team_name]},
                            '$team_b_score',
                            '$team_a_score'
                        ]
                    },
                    'opponent': {
                        '$cond': [
                            {'$eq': ['$team_a_name', team_name]},
                            '$team_b_name',
                            '$team_a_name'
                        ]
                    },
                    'result': '$winner',
                    'win_type': '$win_type',
                    'venue': '$venue'
                }
            },
            {
                '$group': {
                    '_id': '$team',
                    'total_matches': {'$sum': 1},
                    'wins': {'$sum': {'$cond': [{'$eq': ['$result', team_name]}, 1, 0]}},
                    'draws': {'$sum': {'$cond': [{'$eq': ['$result', 'Draw']}, 1, 0]}},
                    'losses': {'$sum': {'$cond': [
                        {'$and': [
                            {'$ne': ['$result', team_name]},
                            {'$ne': ['$result', 'Draw']}
                        ]}, 1, 0
                    ]}},
                    'goals_scored': {'$sum': '$goals_scored'},
                    'goals_conceded': {'$sum': '$goals_conceded'},
                    'world_cup_appearances': {'$addToSet': '$year'}
                }
            },
            {
                '$project': {
                    'team': '$_id',
                    'total_matches': 1,
                    'wins': 1,
                    'draws': 1,
                    'losses': 1,
                    'goals_scored': 1,
                    'goals_conceded': 1,
                    'goal_difference': {'$subtract': ['$goals_scored', '$goals_conceded']},
                    'win_percentage': {
                        '$multiply': [
                            {'$divide': ['$wins', '$total_matches']},
                            100
                        ]
                    },
                    'world_cup_appearances': {'$size': '$world_cup_appearances'}
                }
            }
        ]
        
        collection = self.db_manager.get_collection('matches')
        results = list(collection.aggregate(pipeline))
        return results[0] if results else None
    
    def analyze_stage_statistics(self, year=None):
        """Estatísticas por fase da competição"""
        match_stage = {'$match': {}} if year is None else {'$match': {'year': year}}
        
        pipeline = [
            match_stage,
            {
                '$group': {
                    '_id': '$stage_name_std',
                    'total_matches': {'$sum': 1},
                    'total_goals': {'$sum': '$total_goals'},
                    'avg_goals_per_match': {'$avg': '$total_goals'},
                    'avg_goal_difference': {'$avg': '$goal_difference'},
                    'draws': {'$sum': {'$cond': ['$draw', 1, 0]}},
                    'extra_time_matches': {'$sum': {'$cond': ['$extra_time', 1, 0]}},
                    'penalty_matches': {'$sum': {'$cond': ['$penalty_shootout', 1, 0]}}
                }
            },
            {'$sort': {'total_matches': -1}}
        ]
        
        collection = self.db_manager.get_collection('matches')
        return list(collection.aggregate(pipeline))