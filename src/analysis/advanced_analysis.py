import pandas as pd

from src.database.db import DatabaseManager


class AdvancedAnalyzer:
    def __init__(self):
        self.db_manager = DatabaseManager()
    
    def get_team_goals_timeline(self, team_name):
        """Obtém a linha do tempo de gols de uma equipe"""
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
                    'stage_name': 1,
                    'opponent': {
                        '$cond': [
                            {'$eq': ['$team_a_name', team_name]},
                            '$team_b_name',
                            '$team_a_name'
                        ]
                    }
                }
            },
            {'$sort': {'year': 1}}
        ]
        
        collection = self.db_manager.get_collection('matches')
        return list(collection.aggregate(pipeline))
    
    def get_top_performing_teams(self, limit=10):
        """Ranking das melhores seleções"""
        pipeline = [
            {
                '$group': {
                    '_id': '$winner',
                    'total_wins': {'$sum': 1},
                    'total_matches': {'$sum': 1},
                    'total_goals_scored': {'$sum': {
                        '$cond': [
                            {'$eq': ['$winner', '$team_a_name']},
                            '$team_a_score',
                            '$team_b_score'
                        ]
                    }},
                    'final_wins': {
                        '$sum': {
                            '$cond': [
                                {'$and': [
                                    {'$eq': ['$stage_name', 'Final']},
                                    {'$ne': ['$winner', 'Empate']}
                                ]},
                                1, 0
                            ]
                        }
                    }
                }
            },
            {
                '$match': {
                    '_id': {'$ne': 'Empate'},
                    'total_wins': {'$gte': 5}
                }
            },
            {
                '$project': {
                    'team': '$_id',
                    'total_wins': 1,
                    'final_wins': 1,
                    'win_ratio': {'$divide': ['$total_wins', '$total_matches']},
                    'avg_goals_per_win': {'$divide': ['$total_goals_scored', '$total_wins']}
                }
            },
            {'$sort': {'total_wins': -1}},
            {'$limit': limit}
        ]
        
        collection = self.db_manager.get_collection('matches')
        return list(collection.aggregate(pipeline))
    