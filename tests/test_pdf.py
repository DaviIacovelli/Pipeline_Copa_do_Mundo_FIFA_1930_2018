#!/usr/bin/env python3
"""
Teste para gerar apenas relatórios em PDF
Executa a geração de PDFs sem todo o pipeline de ETL
"""

import os
import sys

# Adicionar src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.analysis.match_analysis import MatchAnalyzer
from src.analysis.tournament_analysis import TournamentAnalyzer
from src.database.db import DatabaseManager
from src.utils.config import Config
from src.visualization.pdfs import PDFGenerator


def test_pdf_generation():
    """Testa a geração completa de PDFs"""
    print("=" * 60)
    print("🧪 TESTE DE GERAÇÃO DE PDFs")
    print("=" * 60)
    
    try:
        # 1. Inicializar componentes
        print("\n✓ Inicializando componentes...")
        pdf_generator = PDFGenerator()
        tournament_analyzer = TournamentAnalyzer()
        match_analyzer = MatchAnalyzer()
        db_manager = DatabaseManager()
        
        # 2. Verificar conexão com banco
        print("✓ Verificando conexão com MongoDB...")
        if not db_manager.test_connection():
            print("✗ Falha na conexão com MongoDB!")
            return False
        
        print("✓ Conexão estabelecida!")
        
        # 3. Gerar relatório de torneio
        print("\n📄 Gerando relatório de torneio...")
        tournament_report = pdf_generator.generate_tournament_report()
        if tournament_report:
            print(f"✓ Relatório de torneio gerado: {tournament_report}")
        else:
            print("✗ Erro ao gerar relatório de torneio")
            return False
        
        # 4. Gerar dados para PDF geral
        print("\n📄 Coletando dados para relatório geral...")
        final_summary = tournament_analyzer.get_tournament_summary()
        
        if not final_summary:
            print("⚠️  Sem dados de resumo do torneio")
        else:
            print(f"✓ Resumo do torneio coletado: {len(final_summary)} edições")
        
        # 5. Coletar dados dos times
        print("\n🏆 Coletando dados dos times...")
        top_teams = ['Brazil', 'Germany', 'Italy', 'Argentina', 'France']
        top_teams_data = []
        
        for team in top_teams:
            stats = tournament_analyzer.get_team_performance(team)
            if stats:
                top_teams_data.append(stats)
                print(f"✓ Dados de {team} coletados")
            else:
                print(f"⚠️  Sem dados para {team}")
        
        # 6. Compilar dados finais
        print("\n📊 Compilando dados finais...")
        final_report = {
            'generated_at': Config.get_current_timestamp(),
            'tournament_summary': final_summary,
            'top_teams': top_teams_data,
            'total_matches_analyzed': sum([e.get('total_matches', 0) for e in final_summary]) if final_summary else 0,
            'total_goals_analyzed': sum([e.get('total_goals', 0) for e in final_summary]) if final_summary else 0
        }
        
        print(f"✓ Relatório final compilado")
        
        # 7. Gerar PDF com dados
        print("\n📄 Gerando PDF com relatório final...")
        pdf_path = pdf_generator.generate_pdf(final_report)
        
        if pdf_path:
            print(f"✓ PDF gerado com sucesso: {pdf_path}")
        else:
            print("✗ Erro ao gerar PDF")
            return False
        
        # 8. Resumo final
        print("\n" + "=" * 60)
        print("✅ TESTE DE PDFs CONCLUÍDO COM SUCESSO!")
        print("=" * 60)
        print(f"\n📁 Arquivos gerados em: {Config.DOCS_PATH}")
        print("   📄 tournament_report_*.pdf")
        print("   📄 relatorio_*.pdf")
        
        # 9. Listar arquivos gerados
        print("\n📋 Arquivos PDF gerados:")
        docs_path = Config.DOCS_PATH
        if os.path.exists(docs_path):
            pdfs = [f for f in os.listdir(docs_path) if f.endswith('.pdf')]
            if pdfs:
                for pdf in sorted(pdfs)[-3:]:  # Mostrar últimos 3
                    pdf_file = os.path.join(docs_path, pdf)
                    size_kb = os.path.getsize(pdf_file) / 1024
                    print(f"   ✓ {pdf} ({size_kb:.1f} KB)")
            else:
                print("   ⚠️  Nenhum PDF encontrado")
        
        return True
        
    except Exception as e:
        print(f"\n✗ ERRO DURANTE O TESTE: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_pdf_from_file():
    """Testa geração de PDF a partir de arquivo JSON"""
    print("\n" + "=" * 60)
    print("🧪 TESTE DE PDF A PARTIR DE ARQUIVO")
    print("=" * 60)
    
    try:
        import json
        from pathlib import Path
        
        pdf_generator = PDFGenerator()
        config = Config()
        
        # Procurar por arquivo JSON processado
        processed_path = Path(config.DATA_PROCESSED_PATH)
        json_files = list(processed_path.glob("*final_analysis*.json"))
        
        if not json_files:
            print("⚠️  Nenhum arquivo final_analysis*.json encontrado")
            print("   Gerando PDF com dados simulados...")
            
            # Dados simulados
            test_data = {
                'tournament_summary': [
                    {'_id': 2022, 'total_matches': 64, 'total_goals': 172},
                    {'_id': 2018, 'total_matches': 64, 'total_goals': 169},
                    {'_id': 2014, 'total_matches': 64, 'total_goals': 171},
                ]
            }
        else:
            latest_file = sorted(json_files)[-1]
            print(f"✓ Arquivo encontrado: {latest_file.name}")
            
            with open(latest_file, 'r') as f:
                test_data = json.load(f)
            
            print(f"✓ Dados carregados: {len(test_data)} seções")
        
        # Gerar PDF
        print("\n📄 Gerando PDF a partir dos dados...")
        pdf_path = pdf_generator.generate_pdf(test_data)
        
        if pdf_path:
            print(f"✓ PDF gerado com sucesso: {pdf_path}")
            size_kb = os.path.getsize(pdf_path) / 1024
            print(f"   Tamanho: {size_kb:.1f} KB")
            return True
        else:
            print("✗ Erro ao gerar PDF")
            return False
            
    except Exception as e:
        print(f"✗ ERRO: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Função principal"""
    print("\n🎯 TESTES DE GERAÇÃO DE PDFs\n")
    print("Opções:")
    print("1. Gerar PDFs com dados do MongoDB")
    print("2. Gerar PDF a partir de arquivo JSON")
    print("3. Ambos os testes")
    print("4. Sair")
    
    choice = input("\nEscolha uma opção (1-4): ").strip()
    
    if choice == '1':
        success = test_pdf_generation()
        return 0 if success else 1
    
    elif choice == '2':
        success = test_pdf_from_file()
        return 0 if success else 1
    
    elif choice == '3':
        success1 = test_pdf_generation()
        print("\n")
        success2 = test_pdf_from_file()
        return 0 if (success1 and success2) else 1
    
    elif choice == '4':
        print("Saindo...")
        return 0
    
    else:
        print("Opção inválida")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
