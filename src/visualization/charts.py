import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
from plotly.subplots import make_subplots

# Configuração do tema
pio.templates.default = "plotly_white"

class ChartGenerator:
    def __init__(self):
        self.color_palette = [
            '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
            '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf'
        ]
    
    def generate_tournament_charts(self, tournament_summary, stage_stats, team_stats=None):
        """Gera todos os gráficos do dashboard"""
        print("Gerando visualizações interativas...")
        
        # 1. Gráfico de evolução de gols
        self._create_goals_evolution_chart(tournament_summary)
        
        # 2. Gráfico de estatísticas por fase
        self._create_stage_stats_chart(stage_stats)
        
        # 3. Gráfico de distribuição de resultados
        self._create_results_distribution_chart(tournament_summary)
        
        # 4. Dashboard resumo
        self._create_summary_dashboard(tournament_summary, stage_stats)
        
        print("Visualizações salvas em 'docs/imagens/'")
    
    def _create_goals_evolution_chart(self, tournament_summary):
        """Gráfico de evolução de gols ao longo das edições"""
        df = pd.DataFrame(tournament_summary)
        
        fig = go.Figure()
        
        # Linha de média de gols
        fig.add_trace(go.Scatter(
            x=df['_id'], 
            y=df['avg_goals_per_match'],
            mode='lines+markers',
            name='Média de Gols por Partida',
            line=dict(color=self.color_palette[0], width=4),
            marker=dict(size=8)
        ))
        
        # Barras de total de gols
        fig.add_trace(go.Bar(
            x=df['_id'],
            y=df['total_goals'],
            name='Total de Gols',
            marker_color=self.color_palette[1],
            opacity=0.7,
            yaxis='y2'
        ))
        
        fig.update_layout(
            title='Evolução dos Gols nas Copas do Mundo',
            xaxis_title='Ano da Copa',
            yaxis_title='Média de Gols por Partida',
            yaxis2=dict(
                title='Total de Gols',
                overlaying='y',
                side='right'
            ),
            hovermode='x unified',
            height=500,
            showlegend=True
        )
        
        # Salvar como HTML interativo e PNG
        fig.write_html("docs/imagens/evolucao_gols.html")
        fig.write_image("docs/imagens/evolucao_gols.png", width=1200, height=500)
    
    def _create_stage_stats_chart(self, stage_stats):
        """Gráfico de estatísticas por fase da competição"""
        df = pd.DataFrame(stage_stats)
        
        # Criar subplots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Total de Partidas', 'Média de Gols por Partida', 
                          'Média de Diferença de Gols', 'Partidas com Prorrogação'),
            specs=[[{"type": "bar"}, {"type": "bar"}],
                   [{"type": "bar"}, {"type": "bar"}]]
        )
        
        # Gráfico 1: Total de partidas
        fig.add_trace(
            go.Bar(x=df['_id'], y=df['total_matches'], 
                   name="Partidas", marker_color=self.color_palette[0]),
            row=1, col=1
        )
        
        # Gráfico 2: Média de gols
        fig.add_trace(
            go.Bar(x=df['_id'], y=df['avg_goals_per_match'],
                   name="Gols/Partida", marker_color=self.color_palette[1]),
            row=1, col=2
        )
        
        # Gráfico 3: Diferença de gols
        fig.add_trace(
            go.Bar(x=df['_id'], y=df['avg_goal_difference'],
                   name="Dif. Gols", marker_color=self.color_palette[2]),
            row=2, col=1
        )
        
        # Gráfico 4: Partidas com prorrogação
        fig.add_trace(
            go.Bar(x=df['_id'], y=df['extra_time_matches'],
                   name="Prorrogações", marker_color=self.color_palette[3]),
            row=2, col=2
        )
        
        fig.update_layout(
            title_text="Estatísticas por Fase da Competição",
            height=600,
            showlegend=False
        )
        
        fig.write_html("docs/imagens/estatisticas_fases.html")
        fig.write_image("docs/imagens/estatisticas_fases.png", width=1200, height=600)
    
    def _create_results_distribution_chart(self, tournament_summary):
        """Gráfico de distribuição de resultados por edição"""
        df = pd.DataFrame(tournament_summary)
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=df['_id'], y=df['matches_with_extra_time'],
            mode='lines+markers',
            name='Partidas com Prorrogação',
            line=dict(dash='dot', color=self.color_palette[2])
        ))
        
        fig.add_trace(go.Scatter(
            x=df['_id'], y=df['matches_with_penalties'],
            mode='lines+markers',
            name='Partidas com Pênaltis',
            line=dict(dash='dash', color=self.color_palette[3])
        ))
        
        fig.update_layout(
            title='Partidas com Prorrogação e Pênaltis por Edição',
            xaxis_title='Ano da Copa',
            yaxis_title='Número de Partidas',
            height=400
        )
        
        fig.write_html("docs/imagens/distribuicao_resultados.html")
        fig.write_image("docs/imagens/distribuicao_resultados.png", width=1200, height=400)
    
    def _create_summary_dashboard(self, tournament_summary, stage_stats):
        """Dashboard completo com múltiplas visualizações"""
        df_tournament = pd.DataFrame(tournament_summary)
        df_stage = pd.DataFrame(stage_stats)
        
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=(
                'Evolução da Média de Gols',
                'Distribuição de Partidas por Fase',
                'Total de Gols por Edição',
                'Estatísticas das Fases'
            ),
            specs=[[{"type": "scatter"}, {"type": "pie"}],
                   [{"type": "bar"}, {"type": "bar"}]]
        )
        
        # Subplot 1: Evolução da média de gols
        fig.add_trace(
            go.Scatter(x=df_tournament['_id'], y=df_tournament['avg_goals_per_match'],
                      mode='lines+markers', name='Média de Gols'),
            row=1, col=1
        )
        
        # Subplot 2: Distribuição por fase (pie chart)
        fig.add_trace(
            go.Pie(labels=df_stage['_id'], values=df_stage['total_matches'],
                   name="Partidas por Fase"),
            row=1, col=2
        )
        
        # Subplot 3: Total de gols por edição
        fig.add_trace(
            go.Bar(x=df_tournament['_id'], y=df_tournament['total_goals'],
                   name='Total de Gols'),
            row=2, col=1
        )
        
        # Subplot 4: Média de gols por fase
        fig.add_trace(
            go.Bar(x=df_stage['_id'], y=df_stage['avg_goals_per_match'],
                   name='Gols por Fase'),
            row=2, col=2
        )
        
        fig.update_layout(
            title_text="Dashboard da Copa do Mundo - Visão Geral",
            height=800,
            showlegend=True
        )
        
        fig.write_html("docs/imagens/dashboard_completo.html")
        fig.write_image("docs/imagens/dashboard_completo.png", width=1400, height=800)
    
    def create_team_analysis_chart(self, team_performance, team_name):
        """Gráfico de desempenho de uma seleção específica"""
        if not team_performance:
            print(f"Dados insuficientes para {team_name}")
            return
        
        labels = ['Vitórias', 'Empates', 'Derrotas']
        values = [
            team_performance['wins'],
            team_performance['draws'],
            team_performance['losses']
        ]
        
        fig = go.Figure(data=[go.Pie(
            labels=labels, 
            values=values,
            hole=.3,
            marker_colors=[self.color_palette[2], self.color_palette[1], self.color_palette[3]]
        )])
        
        fig.update_layout(
            title=f'Desempenho da {team_name} em Copas do Mundo<br>'
                  f'<sub>Total: {team_performance["total_matches"]} jogos | '
                  f'Aproveitamento: {team_performance["win_percentage"]:.1f}%</sub>'
        )
        
        fig.write_html(f"docs/imagens/desempenho_{team_name.lower().replace(' ', '_')}.html")
        fig.write_image(f"docs/imagens/desempenho_{team_name.lower().replace(' ', '_')}.png")
    
    def create_head_to_head_chart(self, head_to_head_stats, team1, team2):
        """Gráfico de confronto direto entre duas seleções"""
        if not head_to_head_stats:
            return
        
        labels = [team1, 'Empates', team2]
        values = [
            head_to_head_stats['team1_wins'],
            head_to_head_stats['draws'],
            head_to_head_stats['team2_wins']
        ]
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=labels,
            y=values,
            marker_color=[self.color_palette[0], self.color_palette[1], self.color_palette[3]],
            text=values,
            textposition='auto',
        ))
        
        fig.update_layout(
            title=f'Confronto Direto: {team1} vs {team2}<br>'
                  f'<sub>Total: {head_to_head_stats["total_matches"]} jogos | '
                  f'Gols: {head_to_head_stats["team1_goals"]}-{head_to_head_stats["team2_goals"]}</sub>',
            xaxis_title='Resultado',
            yaxis_title='Número de Partidas',
            height=400
        )
        
        filename = f"docs/imagens/confronto_{team1.lower().replace(' ', '_')}_vs_{team2.lower().replace(' ', '_')}"
        fig.write_html(f"{filename}.html")
        fig.write_image(f"{filename}.png", width=800, height=400)
    
    def create_goals_timeline(self, matches_data, team_name):
        """Timeline de gols de uma seleção ao longo dos anos"""
        if not matches_data:
            return
        
        # Processar dados para timeline
        years = []
        goals_scored = []
        goals_conceded = []
        
        for match in matches_data:
            years.append(match['year'])
            goals_scored.append(match['goals_scored'])
            goals_conceded.append(match['goals_conceded'])
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=years, y=goals_scored,
            mode='lines+markers',
            name='Gols Marcados',
            line=dict(color=self.color_palette[0], width=3)
        ))
        
        fig.add_trace(go.Scatter(
            x=years, y=goals_conceded,
            mode='lines+markers',
            name='Gols Sofridos',
            line=dict(color=self.color_palette[3], width=3)
        ))
        
        fig.update_layout(
            title=f'Evolução de Gols da {team_name} em Copas do Mundo',
            xaxis_title='Ano',
            yaxis_title='Número de Gols',
            hovermode='x unified',
            height=500
        )
        
        fig.write_html(f"docs/imagens/timeline_gols_{team_name.lower().replace(' ', '_')}.html")
        fig.write_image(f"docs/imagens/timeline_gols_{team_name.lower().replace(' ', '_')}.png")

    
    def create_high_scoring_matches_chart(self, high_scoring_matches):
        """Gráfico de partidas com mais gols"""
        if not high_scoring_matches:
            return
        
        df = pd.DataFrame(high_scoring_matches)
        
        # Preparar dados para o gráfico
        dates = []
        total_goals = []
        match_labels = []
        
        for match in high_scoring_matches:
            match_date = str(match.get('match_date', 'N/A'))[:10]
            team_a = match.get('team_a', 'N/A')
            team_b = match.get('team_b', 'N/A')
            goals = match.get('total_goals', 0)
            
            dates.append(match_date)
            total_goals.append(goals)
            match_labels.append(f"{team_a} vs {team_b}")
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=dates,
            y=total_goals,
            text=match_labels,
            textposition='auto',
            name='Total de Gols',
            marker=dict(
                color=total_goals,
                colorscale='Viridis',
                showscale=True,
                colorbar=dict(title="Gols")
            )
        ))
        
        fig.update_layout(
            title='Partidas com Maior Pontuação da História da Copa do Mundo',
            xaxis_title='Data da Partida',
            yaxis_title='Número de Gols',
            hovermode='x unified',
            height=500,
            showlegend=False
        )
        
        fig.write_html("docs/imagens/partidas_mais_gols.html")
        fig.write_image("docs/imagens/partidas_mais_gols.png", width=1200, height=500)
        return fig
