import json
import os
from datetime import datetime

import pandas as pd

from src.utils.config import Config


class DataManager:
    def __init__(self):
        self.config = Config()
    
    def check_folder_structure(self):
        """Verifica e exibe a estrutura de pastas do projeto"""
        print("📁 ESTRUTURA DE PASTAS DO PROJETO:")
        
        folders = [
            ('data/raw/', 'Dados originais'),
            ('data/processed/', 'Dados processados'),
            ('data/database/', 'Backups do MongoDB'),
            ('docs/imagens/', 'Gráficos e visualizações'),
            ('src/', 'Código fonte'),
            ('tests/', 'Testes unitários')
        ]
        
        for folder_path, description in folders:
            exists = os.path.exists(folder_path)
            status = "✅ EXISTE" if exists else "❌ AUSENTE"
            
            if exists:
                # Contar arquivos
                if os.path.isdir(folder_path):
                    file_count = len([f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))])
                    print(f"   {status} {folder_path} - {description} ({file_count} arquivos)")
                else:
                    print(f"   {status} {folder_path} - {description} (arquivo)")
            else:
                print(f"   {status} {folder_path} - {description}")
    
    def list_processed_files(self):
        """Lista todos os arquivos processados"""
        print("🔍 Procurando arquivos processados...")
        
        if not os.path.exists(self.config.DATA_PROCESSED_PATH):
            print("❌ Pasta de dados processados não existe")
            return []
        
        files = []
        for file in os.listdir(self.config.DATA_PROCESSED_PATH):
            if file.endswith(('.csv', '.json')):
                file_path = os.path.join(self.config.DATA_PROCESSED_PATH, file)
                file_size = os.path.getsize(file_path)
                file_time = datetime.fromtimestamp(os.path.getmtime(file_path))
                
                files.append({
                    'name': file,
                    'size_kb': round(file_size / 1024, 2),
                    'path': file_path,
                    'modified': file_time.strftime("%Y-%m-%d %H:%M:%S")
                })
        
        # Ordenar por data de modificação (mais recente primeiro)
        files.sort(key=lambda x: x['modified'], reverse=True)
        
        for file_info in files:
            print(f"📄 {file_info['name']}")
            print(f"   📏 Tamanho: {file_info['size_kb']} KB")
            print(f"   ⏰ Modificado: {file_info['modified']}")
        
        return files
    
    def list_backups(self):
        """Lista todos os backups do banco"""
        print("🔍 Procurando backups...")
        
        if not os.path.exists(self.config.DATABASE_BACKUP_PATH):
            print("❌ Pasta de backups não existe")
            return []
        
        backups = []
        for backup_folder in os.listdir(self.config.DATABASE_BACKUP_PATH):
            backup_path = os.path.join(self.config.DATABASE_BACKUP_PATH, backup_folder)
            if os.path.isdir(backup_path):
                stats_file = os.path.join(backup_path, 'backup_stats.json')
                if os.path.exists(stats_file):
                    try:
                        with open(stats_file, 'r') as f:
                            stats = json.load(f)
                        backups.append({
                            'folder': backup_folder,
                            'date': stats.get('backup_date', 'Unknown'),
                            'documents': stats.get('total_documents', 0),
                            'collection': stats.get('collection', 'Unknown'),
                            'path': backup_path
                        })
                    except Exception as e:
                        print(f"⚠️  Erro ao ler backup {backup_folder}: {e}")
        
        # Ordenar por data (mais recente primeiro)
        backups.sort(key=lambda x: x['date'], reverse=True)
        
        for backup in backups:
            print(f"📦 {backup['folder']}")
            print(f"   ⏰ Data: {backup['date']}")
            print(f"   📊 Documentos: {backup['documents']}")
            print(f"   🗂️  Coleção: {backup['collection']}")
        
        return backups
    
    def load_latest_processed_data(self):
        """Carrega o arquivo processado mais recente"""
        files = self.list_processed_files()
        if not files:
            return None
        
        # Encontrar o CSV mais recente
        csv_files = [f for f in files if f['name'].endswith('.csv')]
        if not csv_files:
            print("❌ Nenhum arquivo CSV encontrado")
            return None
        
        latest_csv = csv_files[0]  # Já está ordenado por data
        print(f"🔄 Carregando arquivo mais recente: {latest_csv['name']}")
        
        try:
            df = pd.read_csv(latest_csv['path'])
            print(f"✅ Dados carregados: {len(df)} registros")
            return df
        except Exception as e:
            print(f"❌ Erro ao carregar {latest_csv['name']}: {e}")
            return None
    
    def cleanup_old_files(self, keep_recent=3):
        """Remove arquivos antigos, mantendo apenas os mais recentes"""
        print(f"🧹 Limpando arquivos antigos (mantendo {keep_recent} mais recentes)...")
        
        # Limpar arquivos processados
        self._cleanup_folder(self.config.DATA_PROCESSED_PATH, keep_recent)
        
        # Limpar backups
        self._cleanup_folder(self.config.DATABASE_BACKUP_PATH, keep_recent)
        
        print("✅ Limpeza concluída!")
    
    def _cleanup_folder(self, folder_path, keep_recent):
        """Limpa arquivos em uma pasta específica"""
        if not os.path.exists(folder_path):
            print(f"⚠️  Pasta não existe: {folder_path}")
            return
        
        items = []
        for item in os.listdir(folder_path):
            item_path = os.path.join(folder_path, item)
            if os.path.isdir(item_path):
                # Para pastas, usar data de criação
                items.append((item_path, os.path.getctime(item_path), 'folder'))
            else:
                # Para arquivos, usar data de modificação
                items.append((item_path, os.path.getmtime(item_path), 'file'))
        
        if not items:
            print(f"ℹ️  Nenhum item encontrado em {folder_path}")
            return
        
        # Ordenar por data (mais recente primeiro)
        items.sort(key=lambda x: x[1], reverse=True)
        
        # Manter apenas os mais recentes
        items_to_remove = items[keep_recent:]
        
        if not items_to_remove:
            print(f"ℹ️  Nenhum item antigo para remover em {folder_path}")
            return
        
        print(f"🗑️  Removendo {len(items_to_remove)} itens antigos de {folder_path}")
        
        for item_path, _, item_type in items_to_remove:
            try:
                if item_type == 'folder':
                    import shutil
                    shutil.rmtree(item_path)
                    print(f"   📁 Pasta removida: {os.path.basename(item_path)}")
                else:
                    os.remove(item_path)
                    print(f"   📄 Arquivo removido: {os.path.basename(item_path)}")
            except Exception as e:
                print(f"⚠️  Erro ao remover {item_path}: {e}")
    
    def cleanup_images(self):
        """Remove todas as imagens (HTML e PNG) da pasta docs/imagens/"""
        print("🧹 Limpando imagens (.html e .png)...")
        
        images_path = self.config.IMAGES_PATH
        if not os.path.exists(images_path):
            print(f"⚠️  Pasta não existe: {images_path}")
            return
        
        removed_count = 0
        for file in os.listdir(images_path):
            if file.endswith(('.html', '.png')):
                file_path = os.path.join(images_path, file)
                try:
                    os.remove(file_path)
                    print(f"   🗑️  Removido: {file}")
                    removed_count += 1
                except Exception as e:
                    print(f"⚠️  Erro ao remover {file}: {e}")
        
        if removed_count == 0:
            print("ℹ️  Nenhuma imagem encontrada para remover")
        else:
            print(f"✅ Total de imagens removidas: {removed_count}")
    
    def cleanup_pdfs(self):
        """Remove todos os arquivos PDF da pasta docs/"""
        print("🧹 Limpando arquivos PDF...")
        
        docs_path = self.config.DOCS_PATH
        if not os.path.exists(docs_path):
            print(f"⚠️  Pasta não existe: {docs_path}")
            return
        
        removed_count = 0
        for file in os.listdir(docs_path):
            if file.endswith('.pdf'):
                file_path = os.path.join(docs_path, file)
                try:
                    os.remove(file_path)
                    print(f"   📄 Removido: {file}")
                    removed_count += 1
                except Exception as e:
                    print(f"⚠️  Erro ao remover {file}: {e}")
        
        if removed_count == 0:
            print("ℹ️  Nenhum PDF encontrado para remover")
        else:
            print(f"✅ Total de PDFs removidos: {removed_count}")