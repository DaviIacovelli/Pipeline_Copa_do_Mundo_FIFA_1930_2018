import os
import sys

import pandas as pd

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from utils.data_manager import DataManager


def main():
    print("=== GERENCIADOR DE DADOS PROCESSADOS ===\n")
    
    data_manager = DataManager()
    
    while True:
        print("\nOpções:")
        print("1. Listar arquivos processados")
        print("2. Listar backups do banco")
        print("3. Carregar dados processados mais recentes")
        print("4. Limpar arquivos antigos (dados + backups)")
        print("5. Limpar imagens (.html e .png)")
        print("6. Limpar relatórios em PDF")
        print("7. Limpar TUDO (dados + backups + imagens + PDFs)")
        print("8. Sair")
        
        choice = input("\nEscolha uma opção (1-8): ").strip()
        
        if choice == '1':
            data_manager.list_processed_files()
        
        elif choice == '2':
            data_manager.list_backups()
        
        elif choice == '3':
            df = data_manager.load_latest_processed_data()
            if df is not None:
                print(f"\n📋 Informações do dataset carregado:")
                print(f"   📊 Total de registros: {len(df)}")
                if 'year' in df.columns:
                    print(f"   📅 Período: {df['year'].min()} - {df['year'].max()}")
                # Verificar nomes das colunas de times
                team_cols = [col for col in df.columns if 'team' in col.lower() and 'name' in col.lower()]
                if len(team_cols) >= 2:
                    teams = pd.concat([df[team_cols[0]], df[team_cols[1]]], ignore_index=True).unique()
                    print(f"   🌍 Times únicos: {len(teams)}")
                print(f"   📝 Colunas: {', '.join(df.columns.tolist())}")
        
        elif choice == '4':
            keep = input("Manter quantos arquivos recentes? (padrão: 3): ").strip()
            keep = int(keep) if keep.isdigit() else 3
            data_manager.cleanup_old_files(keep_recent=keep)
        
        elif choice == '5':
            data_manager.cleanup_images()
        
        elif choice == '6':
            data_manager.cleanup_pdfs()
        
        elif choice == '7':
            confirm = input("⚠️  Tem certeza que quer limpar TUDO? (s/n): ").strip().lower()
            if confirm == 's':
                keep = input("Manter quantos arquivos recentes? (padrão: 3): ").strip()
                keep = int(keep) if keep.isdigit() else 3
                data_manager.cleanup_old_files(keep_recent=keep)
                data_manager.cleanup_images()
                data_manager.cleanup_pdfs()
                print("✅ Limpeza completa realizada!")
            else:
                print("❌ Operação cancelada")
        
        elif choice == '8':
            print("👋 Até logo!")
            break
        
        else:
            print("❌ Opção inválida")

if __name__ == "__main__":
    main()