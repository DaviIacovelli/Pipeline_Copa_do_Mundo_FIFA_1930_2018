import pandas as pd

from src.database.db import DatabaseManager


class TeamAnalyzer:
    def __init__(self):
        self.db_manager = DatabaseManager()
    
    def get_team_detailed_stats(self, team_name):
        """Estatísticas detalhadas de uma equipe"""
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
                    'is_home': {'$eq': ['$team_a_name', team_name]},
                    'goals_for': {
                        '$cond': [
                            {'$eq': ['$team_a_name', team_name]},
                            '$team_a_score',
                            '$team_b_score'
                        ]
                    },
                    'goals_against': {
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
                    'win_type': 1,
                    'venue': {'$concat': ['$stadium_name', ', ', '$city_name']}
                }
            },
            {
                '$group': {
                    '_id': {
                        'stage': '$stage_name',
                        'year': '$year'
                    },
                    'matches_played': {'$sum': 1},
                    'goals_for': {'$sum': '$goals_for'},
                    'goals_against': {'$sum': '$goals_against'},
                    'wins': {'$sum': {'$cond': [{'$eq': ['$result', team_name]}, 1, 0]}},
                    'clean_sheets': {'$sum': {'$cond': [{'$eq': ['$goals_against', 0]}, 1, 0]}}
                }
            },
            {'$sort': {'_id.year': 1}}
        ]
        
        collection = self.db_manager.get_collection('matches')
        return list(collection.aggregate(pipeline))
    
    def compare_teams(self, team1, team2):
        """Compara duas equipes"""
        stats1 = self.get_team_detailed_stats(team1)
        stats2 = self.get_team_detailed_stats(team2)
        
        comparison = {
            'team1': self._calculate_team_summary(stats1, team1),
            'team2': self._calculate_team_summary(stats2, team2),
            'head_to_head': self._get_head_to_head_stats(team1, team2)
        }
        
        return comparison
    
    def _calculate_team_summary(self, stats, team_name):
        """Calcula resumo da equipe"""
        if not stats:
            return None
        
        total_matches = sum(s['matches_played'] for s in stats)
        total_goals_for = sum(s['goals_for'] for s in stats)
        total_goals_against = sum(s['goals_against'] for s in stats)
        total_wins = sum(s['wins'] for s in stats)
        
        return {
            'team': team_name,
            'total_matches': total_matches,
            'total_goals_for': total_goals_for,
            'total_goals_against': total_goals_against,
            'total_wins': total_wins,
            'win_percentage': (total_wins / total_matches) * 100 if total_matches > 0 else 0,
            'goal_difference': total_goals_for - total_goals_against,
            'avg_goals_for': total_goals_for / total_matches if total_matches > 0 else 0,
            'avg_goals_against': total_goals_against / total_matches if total_matches > 0 else 0
        }
    
    def _get_head_to_head_stats(self, team1, team2):
        """Estatísticas de confronto direto"""
        from src.analysis.match_analysis import MatchAnalyzer
        match_analyzer = MatchAnalyzer()
        return match_analyzer.get_head_to_head(team1, team2)