import os
import sys
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.analysis.match_analysis import MatchAnalyzer
from src.analysis.tournament_analysis import TournamentAnalyzer


class TestAnalysis(unittest.TestCase):
    
    def setUp(self):
        self.tournament_analyzer = TournamentAnalyzer()
        self.match_analyzer = MatchAnalyzer()
    
    def test_tournament_summary(self):
        """Testa resumo do torneio"""
        summary = self.tournament_analyzer.get_tournament_summary()
        self.assertIsInstance(summary, list)
    
    def test_team_performance(self):
        """Testa análise de desempenho de time"""
        # Testar com time conhecido
        performance = self.tournament_analyzer.get_team_performance('Brazil')
        self.assertIsNotNone(performance)
    
    def test_head_to_head(self):
        """Testa confronto direto"""
        h2h = self.match_analyzer.get_head_to_head('Brazil', 'Argentina')
        if h2h:
            self.assertIn('total_matches', h2h)

if __name__ == '__main__':
    unittest.main()