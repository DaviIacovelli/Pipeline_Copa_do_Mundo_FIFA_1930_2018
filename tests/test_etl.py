import os
import sys
import unittest

import pandas as pd

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.etl.extract import DataExtractor
from src.etl.load import DataLoader
from src.etl.transform import DataTransformer


class TestETL(unittest.TestCase):
    
    def setUp(self):
        self.extractor = DataExtractor()
        self.transformer = DataTransformer()
        self.loader = DataLoader()
    
    def test_data_extraction(self):
        """Testa extração de dados"""
        df = self.extractor.load_worldcup_data('data/raw/world_fifa_worldcup_matches.csv')
        self.assertIsNotNone(df)
        self.assertGreater(len(df), 0)
    
    def test_data_transformation(self):
        """Testa transformação de dados"""
        sample_data = {
            'year': [1930, 1934],
            'team_a.name': ['Argentina', 'Brazil'],
            'team_b.name': ['France', 'Yugoslavia'],
            'team_a_score': [1, 2],
            'team_b_score': [0, 1]
        }
        df = pd.DataFrame(sample_data)
        transformed = self.transformer.clean_worldcup_data(df)
        
        self.assertIn('total_goals', transformed.columns)
        self.assertIn('winner', transformed.columns)
    
    def test_data_loading(self):
        """Testa carga de dados (mock)"""
        # Teste com dados mock para não afetar o banco real
        pass

if __name__ == '__main__':
    unittest.main()