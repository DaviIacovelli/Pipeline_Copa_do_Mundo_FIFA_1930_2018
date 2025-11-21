import os
import sys
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.visualization.charts import ChartGenerator


class TestVisualization(unittest.TestCase):
    
    def setUp(self):
        self.chart_generator = ChartGenerator()
    
    def test_chart_creation(self):
        """Testa criação de gráficos"""
        sample_data = [
            {'_id': 2018, 'total_matches': 64, 'total_goals': 169, 'avg_goals_per_match': 2.64},
            {'_id': 2014, 'total_matches': 64, 'total_goals': 171, 'avg_goals_per_match': 2.67}
        ]
        
        # Testar se os gráficos são criados sem erros
        try:
            self.chart_generator._create_goals_evolution_chart(sample_data)
            chart_created = True
        except:
            chart_created = False
        
        self.assertTrue(chart_created)

if __name__ == '__main__':
    unittest.main()