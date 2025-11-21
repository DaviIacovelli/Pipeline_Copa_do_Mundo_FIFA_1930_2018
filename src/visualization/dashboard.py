import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from src.database.db import DatabaseManager
from src.utils.config import Config


class InteractiveDashboard:
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.config = Config()
    
    def create_main_dashboard(self):
        """Cria dashboard principal interativo"""
        # Coletar dados
        tournament_data = self._get_tournament_data()
        team_data = self._get_team_stats()
        match_data = self._get_recent_matches()
        
        # Criar layout do dashboard
        fig = make_subplots(
            rows=3, cols=3,
            specs=[
                [{"type": "bar", "colspan": 2}, None, {"type": "pie"}],
                [{"type": "scatter", "colspan": 3}, None, None],
                [{"type": "table", "colspan": 3}, None, None]
            ],
            subplot_titles=(
                'Títulos por País', 'Distribuição de Fases',
                'Evolução de Gols por Edição', 'Últimas Partidas'
            ),
            vertical_spacing=0.08,
            horizontal_spacing=0.05
        )
        
        # Gráfico 1: Títulos por país
        fig.add_trace(self._create_champions_chart(team_data), row=1, col=1)
        
        # Gráfico 2: Distribuição de fases
        fig.add_trace(self._create_stage_distribution(tournament_data), row=1, col=3)
        
        # Gráfico 3: Evolução de gols
        fig.add_trace(self._create_goals_evolution(tournament_data), row=2, col=1)
        
        # Gráfico 4: Tabela de partidas recentes
        fig.add_trace(self._create_matches_table(match_data), row=3, col=1)
        
        fig.update_layout(
            title_text="Dashboard Interativo - Copa do Mundo FIFA",
            height=1000,
            showlegend=True,
            template="plotly_white"
        )
        
        # Salvar dashboard
        fig.write_html(f"{self.config.IMAGES_PATH}dashboard_interativo.html")
        print("Dashboard interativo criado!")
    
    def _get_tournament_data(self):
        """Obtém dados dos torneios"""
        pipeline = [
            {
                '$group': {
                    '_id': '$year',
                    'total_matches': {'$sum': 1},
                    'total_goals': {'$sum': '$total_goals'},
                    'avg_goals': {'$avg': '$total_goals'}
                }
            }
        ]
        collection = self.db_manager.get_collection('matches')
        return list(collection.aggregate(pipeline))
    
    def _get_team_stats(self):
        """Obtém estatísticas das equipes"""
        pipeline = [
            {
                '$group': {
                    '_id': '$winner',
                    'titles': {'$sum': 1}
                }
            },
            {
                '$match': {'_id': {'$ne': None}}
            },
            {
                '$sort': {'titles': -1}
            },
            {
                '$limit': 15
            }
        ]
        collection = self.db_manager.get_collection('matches')
        return list(collection.aggregate(pipeline))
    
    def _get_recent_matches(self):
        """Obtém partidas recentes"""
        collection = self.db_manager.get_collection('matches')
        recent_matches = list(
            collection.find()
            .sort('match_date', -1)
            .limit(10)
        )
        return recent_matches
    
    def _create_champions_chart(self, data):
        """Cria gráfico de campeões"""
        if not data:
            return go.Bar()
        
        df = pd.DataFrame(data)
        df.rename(columns={'_id': 'country', 'titles': 'titles'}, inplace=True)
        
        return go.Bar(
            x=df['country'],
            y=df['titles'],
            name='Títulos',
            marker=dict(color='#1f77b4'),
            text=df['titles'],
            textposition='auto'
        )
    
    def _create_stage_distribution(self, data):
        """Cria gráfico de distribuição de fases"""
        pipeline = [
            {
                '$group': {
                    '_id': '$stage_name',
                    'count': {'$sum': 1}
                }
            },
            {
                '$sort': {'count': -1}
            }
        ]
        collection = self.db_manager.get_collection('matches')
        stage_data = list(collection.aggregate(pipeline))
        
        if not stage_data:
            return go.Pie()
        
        df = pd.DataFrame(stage_data)
        df.rename(columns={'_id': 'stage', 'count': 'matches'}, inplace=True)
        
        return go.Pie(
            labels=df['stage'],
            values=df['matches'],
            name='Fases',
            textinfo='label+percent'
        )
    
    def _create_goals_evolution(self, data):
        """Cria gráfico de evolução de gols"""
        if not data:
            return go.Scatter()
        
        df = pd.DataFrame(data)
        df.rename(columns={'_id': 'year'}, inplace=True)
        df = df.sort_values('year')
        
        return go.Scatter(
            x=df['year'],
            y=df['total_goals'],
            mode='lines+markers',
            name='Total de Gols',
            line=dict(color='#ff7f0e', width=2),
            marker=dict(size=8),
            fill='tozeroy'
        )
    
    def _create_matches_table(self, data):
        """Cria tabela de partidas"""
        if not data:
            return go.Table()
        
        df = pd.DataFrame(data)
        
        # Selecionar colunas relevantes
        cols_to_show = ['match_date', 'stage_name', 'team_a', 'team_b', 'result']
        available_cols = [col for col in cols_to_show if col in df.columns]
        
        df_display = df[available_cols].head(10)
        
        return go.Table(
            header=dict(
                values=['<b>' + col.replace('_', ' ').title() + '</b>' for col in df_display.columns],
                fill_color='#1f77b4',
                align='center',
                font=dict(color='white', size=12)
            ),
            cells=dict(
                values=[df_display[col] for col in df_display.columns],
                fill_color='lavender',
                align='center',
                font=dict(size=11)
            )
        )