from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.platypus import (Image, PageBreak, Paragraph, Preformatted,
                                SimpleDocTemplate, Spacer, Table, TableStyle)

from src.database.db import DatabaseManager
from src.utils.config import Config


class PDFGenerator:
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.config = Config()
        self.styles = getSampleStyleSheet()
        self._create_custom_styles()
    
    def _create_custom_styles(self):
        """Cria estilos personalizados para o PDF"""
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1f77b4'),
            spaceAfter=30,
            alignment=1  # Centralizado
        ))
        
        self.styles.add(ParagraphStyle(
            name='CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#1f77b4'),
            spaceAfter=12,
            spaceBefore=12
        ))
        
        self.styles.add(ParagraphStyle(
            name='CustomBody',
            parent=self.styles['Normal'],
            fontSize=11,
            alignment=4  # Justificado
        ))

    def generate_pdf(self, data, output_file=None, path=None):
        """Gera PDF a partir de dados"""
        try:
            if output_file is None:
                output_file = f"{self.config.DOCS_PATH}relatorio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            
            doc = SimpleDocTemplate(
                output_file,
                pagesize=A4,
                leftMargin=20*mm,
                rightMargin=20*mm,
                topMargin=20*mm,
                bottomMargin=20*mm
            )
            
            story = []
            
            # Adicionar cabeçalho
            story.append(Paragraph("Relatório - Copa do Mundo FIFA", self.styles['CustomTitle']))
            story.append(Paragraph(f"Gerado em {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}", 
                                 self.styles['CustomHeading']))
            story.append(Spacer(1, 20))
            
            # Processar dados
            if isinstance(data, str):
                story.append(Paragraph(data, self.styles['CustomBody']))
            elif isinstance(data, dict):
                story.extend(self._process_dict_data(data))
            elif isinstance(data, list):
                story.extend(self._process_list_data(data))
            else:
                story.append(Paragraph(str(data), self.styles['CustomBody']))
            
            # Construir PDF
            doc.build(story)
            print(f"✓ PDF gerado com sucesso: {output_file}")
            return output_file
            
        except Exception as e:
            print(f"✗ Erro ao gerar PDF: {e}")
            return None
    
    def _process_dict_data(self, data):
        """Processa dados em formato de dicionário"""
        elements = []
        
        for key, value in data.items():
            # Se a chave não é especial (como summary, top_teams, etc)
            if isinstance(value, dict) and not isinstance(value, (int, float, str)):
                elements.append(Paragraph(f"<b>{key}</b>", self.styles['CustomHeading']))
                elements.extend(self._create_table_from_dict(value))
            elif isinstance(value, list):
                elements.append(Paragraph(f"<b>{key}</b>", self.styles['CustomHeading']))
                # Se é lista de dicionários, criar tabelas
                if value and isinstance(value[0], dict):
                    for item in value:
                        elements.extend(self._create_table_from_dict(item))
                        elements.append(Spacer(1, 12))
                else:
                    elements.extend(self._process_list_data(value))
            else:
                elements.append(Paragraph(str(value), self.styles['CustomBody']))
            
            elements.append(Spacer(1, 12))
        
        return elements
    
    def _process_list_data(self, data):
        """Processa dados em formato de lista"""
        elements = []
        
        for item in data:
            if isinstance(item, dict):
                elements.extend(self._create_table_from_dict(item))
            else:
                elements.append(Paragraph(str(item), self.styles['CustomBody']))
            
            elements.append(Spacer(1, 8))
        
        return elements
    
    def _create_table_from_dict(self, data):
        """Cria uma tabela a partir de um dicionário"""
        elements = []
        
        table_data = [['Descrição', 'Valor']]
        for k, v in data.items():
            table_data.append([str(k), str(v)])
        
        table = Table(table_data, colWidths=[200, 250])
        
        table.setStyle(TableStyle([
            # Cabeçalho (linha 0)
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f77b4')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('ALIGNMENT', (0, 0), (-1, 0), 'CENTER'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('TOPPADDING', (0, 0), (-1, 0), 8),
            # Coluna esquerda dados (a partir linha 1)
            ('BACKGROUND', (0, 1), (0, -1), colors.HexColor('#e8f0f7')),
            ('TEXTCOLOR', (0, 1), (0, -1), colors.black),
            ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
            # Coluna direita dados
            ('BACKGROUND', (1, 1), (1, -1), colors.white),
            ('TEXTCOLOR', (1, 1), (1, -1), colors.black),
            # Alinhamento geral
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            # Grid
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f5f5f5')])
        ]))
        
        elements.append(table)
        return elements
    
    def generate_tournament_report(self, year=None, output_file=None):
        """Gera relatório completo do torneio"""
        try:
            if output_file is None:
                output_file = f"{self.config.DOCS_PATH}tournament_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            
            doc = SimpleDocTemplate(output_file, pagesize=A4, leftMargin=20*mm, rightMargin=20*mm)
            story = []
            
            # Título
            story.append(Paragraph("Relatório Completo - Copa do Mundo FIFA", self.styles['CustomTitle']))
            story.append(Paragraph(f"Data: {datetime.now().strftime('%d/%m/%Y')}", self.styles['Normal']))
            story.append(Spacer(1, 20))
            
            # Estatísticas Gerais
            story.append(Paragraph("Estatísticas Gerais", self.styles['CustomHeading']))
            general_stats = self._get_general_statistics()
            if general_stats:
                story.extend(self._create_table_from_dict(general_stats))
            story.append(Spacer(1, 20))
            
            # Campeões
            story.append(PageBreak())
            story.append(Paragraph("Campeões por Título", self.styles['CustomHeading']))
            champions = self._get_champions_data()
            if champions:
                champions_table = self._create_champions_table(champions)
                if champions_table:
                    story.append(champions_table)
                else:
                    story.append(Paragraph("Sem dados de campeões disponíveis", self.styles['Normal']))
            else:
                story.append(Paragraph("Sem dados de campeões disponíveis", self.styles['Normal']))
            story.append(Spacer(1, 20))
            
            # Partidas Destacadas
            story.append(Paragraph("Partidas com Maior Pontuação", self.styles['CustomHeading']))
            high_scoring = self._get_high_scoring_matches()
            if high_scoring:
                matches_table = self._create_matches_table(high_scoring)
                if matches_table:
                    story.append(matches_table)
                else:
                    story.append(Paragraph("Sem dados de partidas disponíveis", self.styles['Normal']))
            else:
                story.append(Paragraph("Sem dados de partidas disponíveis", self.styles['Normal']))
            
            doc.build(story)
            print(f"✓ Relatório do torneio gerado: {output_file}")
            return output_file
            
        except Exception as e:
            print(f"✗ Erro ao gerar relatório: {e}")
            return None
    
    def _get_general_statistics(self):
        """Obtém estatísticas gerais do banco"""
        try:
            collection = self.db_manager.get_collection('matches')
            stats = collection.aggregate([
                {
                    '$group': {
                        '_id': None,
                        'total_matches': {'$sum': 1},
                        'total_goals': {'$sum': '$total_goals'},
                        'avg_goals': {'$avg': '$total_goals'}
                    }
                }
            ])
            
            result = list(stats)
            if result:
                data = result[0]
                return {
                    'Total de Partidas': int(data.get('total_matches', 0)),
                    'Total de Gols': int(data.get('total_goals', 0)),
                    'Média de Gols por Partida': f"{data.get('avg_goals', 0):.2f}"
                }
        except Exception as e:
            print(f"Erro ao obter estatísticas gerais: {e}")
        
        return None
    
    def _get_champions_data(self):
        """Obtém dados dos campeões"""
        try:
            collection = self.db_manager.get_collection('matches')
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
                    '$limit': 10
                }
            ]
            
            return list(collection.aggregate(pipeline))
        except Exception as e:
            print(f"Erro ao obter dados dos campeões: {e}")
            return []
    
    def _get_high_scoring_matches(self):
        """Obtém partidas com maior pontuação"""
        try:
            collection = self.db_manager.get_collection('matches')
            return list(
                collection.find()
                .sort('total_goals', -1)
                .limit(10)
            )
        except Exception as e:
            print(f"Erro ao obter partidas de alto score: {e}")
            return []
    
    def _create_champions_table(self, data):
        """Cria tabela de campeões"""
        if not data:
            return None
            
        table_data = [['País', 'Títulos']]
        
        for item in data:
            country = item.get('_id') or 'N/A'
            titles = item.get('titles', 0)
            if country and country != 'None':
                table_data.append([str(country), str(titles)])
        
        if len(table_data) <= 1:  # Se só tem cabeçalho, retorna None
            return None
        
        table = Table(table_data, colWidths=[200, 100])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f77b4')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f0f0')])
        ]))
        
        return table
    
    def _create_matches_table(self, data):
        """Cria tabela de partidas"""
        if not data:
            return None
            
        table_data = [['Data', 'Fase', 'Time A', 'Time B', 'Gols']]
        
        for match in data:
            match_date = str(match.get('match_date', 'N/A'))[:10] if match.get('match_date') else 'N/A'
            stage = str(match.get('stage_name', 'N/A')) if match.get('stage_name') else 'N/A'
            team_a = str(match.get('team_a', 'N/A')) if match.get('team_a') else 'N/A'
            team_b = str(match.get('team_b', 'N/A')) if match.get('team_b') else 'N/A'
            goals = str(match.get('total_goals', 0)) if match.get('total_goals') is not None else '0'
            
            table_data.append([match_date, stage, team_a, team_b, goals])
        
        if len(table_data) <= 1:  # Se só tem cabeçalho, retorna None
            return None
        
        table = Table(table_data, colWidths=[80, 80, 80, 80, 50])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f77b4')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f0f0')])
        ]))
        
        return table