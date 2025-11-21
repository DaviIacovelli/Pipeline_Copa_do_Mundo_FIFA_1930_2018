import json
import os
from datetime import datetime

import pandas as pd

from src.database.db import DatabaseManager
from src.utils.config import Config


class DataLoader:
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.config = Config()
    
    def load_matches_to_mongodb(self, df, collection_name='matches'):
        """Carrega dados das partidas para MongoDB e salva arquivos processados"""
        try:
            collection = self.db_manager.get_collection(collection_name)
            
            # Limpar coleção existente
            collection.delete_many({})
            
            # Converter para dicionário
            records = df.to_dict('records')
            
            # Inserir dados
            result = collection.insert_many(records)
            print(f"✅ {len(result.inserted_ids)} partidas carregadas no MongoDB")
            
            # Criar índices
            self.db_manager.create_indexes()
            
            # Salvar dados processados
            self._save_processed_data(df, records)
            
            # Fazer backup do MongoDB
            self._backup_database(collection_name)
            
            return True
            
        except Exception as e:
            print(f"❌ Erro ao carregar dados: {e}")
            return False
    
    def _save_processed_data(self, df, records):
        """Salva dados processados em diferentes formatos"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # 1. Salvar como CSV processado
            csv_path = os.path.join(self.config.DATA_PROCESSED_PATH, f'worldcup_matches_processed_{timestamp}.csv')
            df.to_csv(csv_path, index=False, encoding='utf-8')
            print(f"💾 CSV processado salvo: {csv_path}")
            
            # 2. Salvar como JSON
            json_path = os.path.join(self.config.DATA_PROCESSED_PATH, f'worldcup_matches_processed_{timestamp}.json')
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(records, f, indent=2, ensure_ascii=False, default=str)
            print(f"💾 JSON processado salvo: {json_path}")
            
            # 3. Salvar arquivo de metadados
            metadata = {
                'processing_date': timestamp,
                'total_matches': len(df),
                'years_covered': f"{df['year'].min()}-{df['year'].max()}",
                'total_teams': pd.concat([df['team_a_name'], df['team_b_name']]).nunique(),
                'columns_processed': list(df.columns)
            }
            
            metadata_path = os.path.join(self.config.DATA_PROCESSED_PATH, f'processing_metadata_{timestamp}.json')
            with open(metadata_path, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)
            print(f"📊 Metadados salvos: {metadata_path}")
            
        except Exception as e:
            print(f"⚠️  Erro ao salvar dados processados: {e}")
    
    def _backup_database(self, collection_name):
        """Faz backup dos dados do MongoDB"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_dir = os.path.join(self.config.DATABASE_BACKUP_PATH, f'backup_{timestamp}')
            os.makedirs(backup_dir, exist_ok=True)
            
            collection = self.db_manager.get_collection(collection_name)
            records = list(collection.find({}))
            
            # Salvar backup completo
            backup_path = os.path.join(backup_dir, f'{collection_name}_backup.json')
            with open(backup_path, 'w', encoding='utf-8') as f:
                json.dump(records, f, indent=2, ensure_ascii=False, default=str)
            
            # Salvar estatísticas do backup
            stats = {
                'backup_date': timestamp,
                'collection': collection_name,
                'total_documents': len(records),
                'database': self.db_manager.database_name
            }
            
            stats_path = os.path.join(backup_dir, 'backup_stats.json')
            with open(stats_path, 'w', encoding='utf-8') as f:
                json.dump(stats, f, indent=2, ensure_ascii=False)
            
            print(f"📦 Backup do MongoDB salvo: {backup_dir}")
            print(f"   📁 Documentos: {len(records)}")
            
        except Exception as e:
            print(f"⚠️  Erro ao fazer backup: {e}")
    
    def export_analysis_data(self, analysis_results, filename):
        """Exporta resultados de análise para a pasta processed"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_path = os.path.join(self.config.DATA_PROCESSED_PATH, f'{filename}_{timestamp}.json')
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(analysis_results, f, indent=2, ensure_ascii=False, default=str)
            
            print(f"📈 Dados de análise exportados: {file_path}")
            return file_path
            
        except Exception as e:
            print(f"⚠️  Erro ao exportar análise: {e}")
            return None
    
    def verify_data_loading(self, collection_name='matches'):
        """Verifica se os dados foram carregados corretamente"""
        try:
            collection = self.db_manager.get_collection(collection_name)
            count = collection.count_documents({})
            print(f"✅ Verificação: {count} documentos na coleção '{collection_name}'")
            
            # Estatísticas básicas
            pipeline = [
                {
                    '$group': {
                        '_id': None,
                        'total_goals': {'$sum': '$total_goals'},
                        'avg_goals_per_match': {'$avg': '$total_goals'},
                        'unique_teams': {
                            '$addToSet': '$team_a_name'
                        }
                    }
                }
            ]
            
            stats = list(collection.aggregate(pipeline))
            if stats:
                stats = stats[0]
                unique_teams = len(stats['unique_teams']) * 2  # Aproximação
                print(f"📊 Estatísticas:")
                print(f"   🥅 Total de gols: {stats['total_goals']}")
                print(f"   📈 Média de gols/partida: {stats['avg_goals_per_match']:.2f}")
                print(f"   🌍 Times únicos: ~{unique_teams}")
            
            return True
        except Exception as e:
            print(f"❌ Erro na verificação: {e}")
            return False
        
