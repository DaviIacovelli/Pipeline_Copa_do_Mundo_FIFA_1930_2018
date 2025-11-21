import os
import sys

from src.analysis.advanced_analysis import AdvancedAnalyzer
from src.analysis.match_analysis import MatchAnalyzer
from src.analysis.tournament_analysis import TournamentAnalyzer
from src.etl.extract import DataExtractor
from src.etl.load import DataLoader
from src.etl.transform import DataTransformer
from src.utils.config import Config
from src.utils.data_manager import DataManager
from src.visualization.charts import ChartGenerator
from src.visualization.dashboard import InteractiveDashboard
from src.visualization.pdfs import PDFGenerator


def setup_environment():
    """Configura o ambiente e verifica dependências"""
    print("=== CONFIGURAÇÃO DO AMBIENTE ===")
    
    # Criar diretórios
    Config.create_directories()
    
    # Verificar se o arquivo de dados existe
    data_file = 'data/raw/world_fifa_worldcup_matches.csv'
    if not os.path.exists(data_file):
        print(f"❌ Arquivo de dados não encontrado: {data_file}")
        print("  Certifique-se de que o arquivo CSV está na pasta data/raw/")
        return False
    
    # Inicializar gerenciador de dados
    data_manager = DataManager()
    
    # Verificar se existem dados processados recentes
    print("\n=== VERIFICAÇÃO DE DADOS EXISTENTES ===")
    processed_files = data_manager.list_processed_files()
    backups = data_manager.list_backups()
    
    if processed_files:
        print(f"📁 Encontrados {len(processed_files)} arquivos processados")
    else:
        print("📁 Nenhum arquivo processado encontrado")
    
    if backups:
        print(f"📦 Encontrados {len(backups)} backups do banco")
    else:
        print("📦 Nenhum backup encontrado")
    
    print("✅ Ambiente configurado com sucesso!")
    return True

def run_etl_pipeline():
    """Executa o pipeline completo de ETL"""
    print("\n" + "="*50)
    print("1. EXTRACT, TRANSFORM, LOAD")
    print("="*50)
    
    extractor = DataExtractor()
    transformer = DataTransformer()
    loader = DataLoader()
    
    # Carregar dados
    print("📥 Extraindo dados...")
    raw_data = extractor.load_worldcup_data('data/raw/world_fifa_worldcup_matches.csv')
    extractor.analyze_dataset(raw_data)
    
    # Transformar dados
    print("🔄 Transformando dados...")
    transformed_data = transformer.clean_worldcup_data(raw_data)
    
    # Carregar no MongoDB e salvar processados
    print("📤 Carregando dados no MongoDB...")
    success = loader.load_matches_to_mongodb(transformed_data)
    if not success:
        print("❌ Falha no carregamento dos dados")
        return False
        
    loader.verify_data_loading()
    return True

def run_data_analysis():
    """Executa todas as análises de dados"""
    print("\n" + "="*50)
    print("2. ANÁLISE DE DADOS")
    print("="*50)
    
    tournament_analyzer = TournamentAnalyzer()
    match_analyzer = MatchAnalyzer()
    loader = DataLoader()
    
    # Coletar dados para análise
    print("📊 Coletando estatísticas do torneio...")
    tournament_summary = tournament_analyzer.get_tournament_summary()
    stage_stats = tournament_analyzer.analyze_stage_statistics()
    
    # Exportar dados de análise
    print("💾 Exportando dados de análise...")
    loader.export_analysis_data(tournament_summary, 'tournament_summary')
    loader.export_analysis_data(stage_stats, 'stage_statistics')
    
    # Análises específicas
    print("\n🔍 Realizando análises específicas...")
    
    # Times para análise
    teams_to_analyze = ['Brazil', 'Germany', 'Argentina', 'Italy', 'France', 'Spain', 'England', 'Netherlands']
    
    for team in teams_to_analyze:
        print(f"   ⚽ Analisando {team}...")
        team_performance = tournament_analyzer.get_team_performance(team)
        if team_performance:
            # Exportar dados do time
            loader.export_analysis_data(team_performance, f'team_performance_{team}')
            print(f"   ✅ Dados de {team} exportados")
        else:
            print(f"   ⚠️  Dados insuficientes para {team}")
    
    # Partidas de alto placar
    print("\n🎯 Identificando partidas memoráveis...")
    high_scoring_matches = match_analyzer.get_high_scoring_matches(min_goals=6, limit=5)
    loader.export_analysis_data(high_scoring_matches, 'high_scoring_matches')
    
    # Análise das finais
    finals_analysis = match_analyzer.analyze_final_matches()
    loader.export_analysis_data(finals_analysis, 'world_cup_finals')
    
    print("✅ Análises concluidas com sucesso!")
    return tournament_summary, stage_stats

def run_visualizations(tournament_summary, stage_stats):
    """Gera todas as visualizações"""
    print("\n" + "="*50)
    print("3. VISUALIZAÇÕES INTERATIVAS")
    print("="*50)
    
    chart_generator = ChartGenerator()
    tournament_analyzer = TournamentAnalyzer()
    match_analyzer = MatchAnalyzer()
    
    print("📈 Gerando gráficos principais...")
    chart_generator.generate_tournament_charts(tournament_summary, stage_stats)
    
    # Gráficos específicos de times
    print("\n🏆 Gerando gráficos de times...")
    top_teams = ['Brazil', 'Germany', 'Argentina', 'Italy']
    
    for team in top_teams:
        team_performance = tournament_analyzer.get_team_performance(team)
        if team_performance:
            chart_generator.create_team_analysis_chart(team_performance, team)
            print(f"   ✅ Gráfico gerado para {team}")
    
    # Gráficos de confrontos clássicos
    print("\n⚔️ Gerando gráficos de confrontos...")
    classic_matches = [
        ('Brazil', 'Germany'),
        ('Argentina', 'England'),
        ('Italy', 'France'),
        ('Netherlands', 'Spain')
    ]
    
    for team1, team2 in classic_matches:
        h2h = match_analyzer.get_head_to_head(team1, team2)
        if h2h and h2h['total_matches'] > 0:
            chart_generator.create_head_to_head_chart(h2h, team1, team2)
            print(f"   ✅ Confronto {team1} vs {team2}")
    

    print("\n📊 Gerando gráficos de partidas de alto placar...")
    high_scoring_matches = match_analyzer.get_high_scoring_matches(limit=5)
    chart_generator.create_high_scoring_matches_chart(high_scoring_matches)
    
    # Dashboard Interativo
    print("\n🎯 Gerando dashboard interativo...")
    dashboard = InteractiveDashboard()
    dashboard.create_main_dashboard()

    print("✅ Todas as visualizações geradas!")

def run_team_detailed_analysis():
    """Análise detalhada de times específicos"""
    print("\n" + "="*50)
    print("4. ANÁLISE DETALHADA DE TIMES")
    print("="*50)
    
    advanced_analyzer = AdvancedAnalyzer()
    tournament_analyzer = TournamentAnalyzer()
    chart_generator = ChartGenerator()
    loader = DataLoader()
    
    # Times para análise detalhada
    focus_teams = ['Brazil', 'Germany', 'Argentina']
    
    for team in focus_teams:
        print(f"\n🔍 Análise detalhada: {team}")
        
        # Timeline de gols
        goals_timeline = advanced_analyzer.get_team_goals_timeline(team)
        if goals_timeline:
            loader.export_analysis_data(goals_timeline, f'goals_timeline_{team}')
            chart_generator.create_goals_timeline(goals_timeline, team)
            print(f"   📅 Timeline de gols gerada para {team}")
        
        # Performance por fase
        team_stats = tournament_analyzer.get_team_performance(team)
        if team_stats:
            loader.export_analysis_data(team_stats, f'team_performance_{team}')
            chart_generator.create_team_analysis_chart(team_stats, team)
            print(f"   📊 Estatísticas de {team}:")
            print(f"      🏃 Partidas: {team_stats['total_matches']}")
            print(f"      ✅ Vitórias: {team_stats['wins']} ({team_stats['win_percentage']:.1f}%)")
            print(f"      🥅 Gols: {team_stats['goals_scored']} marcados, {team_stats['goals_conceded']} sofridos")
            print(f"      🌍 Copas: {team_stats.get('world_cup_appearances', 'N/A')} participações")

def generate_final_reports():
    """Gera relatórios finais e faz limpeza"""
    print("\n" + "="*50)
    print("5. RELATÓRIOS FINAIS E LIMPEZA")
    print("="*50)
    
    data_manager = DataManager()
    tournament_analyzer = TournamentAnalyzer()
    pdf_generator = PDFGenerator()
    loader = DataLoader()
    
    # Gerar relatório consolidado
    print("📋 Gerando relatório consolidado...")
    
    # Coletar dados finais
    final_summary = tournament_analyzer.get_tournament_summary()
    top_teams_data = []
    
    top_teams = ['Brazil', 'Germany', 'Italy', 'Argentina', 'France']
    for team in top_teams:
        stats = tournament_analyzer.get_team_performance(team)
        if stats:
            top_teams_data.append(stats)
    
    final_report = {
        'generated_at': Config.get_current_timestamp(),
        'tournament_summary': final_summary,
        'top_teams': top_teams_data,
        'total_matches_analyzed': sum(edition['total_matches'] for edition in final_summary),
        'total_goals_analyzed': sum(edition['total_goals'] for edition in final_summary)
    }
    
    loader.export_analysis_data(final_report, 'final_analysis_report')

    # Gerar PDF com dados
    print("📄 Gerando relatório em PDF...")
    pdf_generator.generate_tournament_report()
    
    # Gerar PDF padrão com resumo
    pdf_generator.generate_pdf(final_report)
    
    # Limpeza de arquivos antigos
    print("🧹 Realizando limpeza de arquivos antigos...")
    data_manager.cleanup_old_files(keep_recent=3)
    
    # Listar resultados finais
    print("\n📊 RESUMO FINAL:")
    data_manager.list_processed_files()
    data_manager.list_backups()

def main():
    """Função principal"""
    print("=== ANÁLISE DA COPA DO MUNDO FIFA ===")
    print("📊 Sistema de Análise de Dados Históricos")
    print("="*50)
    
    # Configurar ambiente
    if not setup_environment():
        sys.exit(1)
    
    try:
        # 1. ETL Pipeline
        if not run_etl_pipeline():
            sys.exit(1)
        
        # 2. Análise de Dados
        tournament_summary, stage_stats = run_data_analysis()
        
        # 3. Análise Detalhada
        run_team_detailed_analysis()
        
        # 4. Visualizações
        run_visualizations(tournament_summary, stage_stats)
        
        # 5. Relatórios Finais
        generate_final_reports()
        
        # Mensagem final
        print("\n" + "🎉" * 20)
        print("🎉 ANÁLISE COMPLETA COM SUCESSO! 🎉")
        print("🎉" * 20)
        
        print("\n📁 ESTRUTURA DE ARQUIVOS GERADOS:")
        print("   📂 data/processed/    - Dados processados e análises")
        print("   📂 data/database/     - Backups do MongoDB") 
        print("   📂 docs/imagens/      - Gráficos e visualizações")
        print("   📂 docs/              - Relatórios em PDF e Dashboard")
        print("   📄 data/raw/          - Dados originais (mantido)")
        
        print("\n🔍 PRÓXIMOS PASSOS:")
        print("   1. Verifique o dashboard em 'docs/dashboard_interativo.html'")
        print("   2. Consulte os relatórios em PDF em 'docs/'")
        print("   3. Veja os gráficos em 'docs/imagens/'")
        print("   4. Consulte os dados processados em 'data/processed/'")
        print("   5. Execute 'python manage_data.py' para gerenciar arquivos")
        print("   6. Verifique o MongoDB para dados atualizados")
        
    except Exception as e:
        print(f"\n❌ ERRO DURANTE A EXECUÇÃO: {e}")
        print("💡 Possíveis soluções:")
        print("   - Verifique a conexão com o MongoDB")
        print("   - Confirme que o arquivo CSV está correto")
        print("   - Execute 'python manage_data.py' para limpar dados corrompidos")
        sys.exit(1)

if __name__ == "__main__":
    main()