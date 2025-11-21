import re
from datetime import datetime

import pandas as pd


def format_team_name(team_name):
    """Padroniza nomes de times"""
    name_mapping = {
        'West Germany': 'Germany',
        'West Germany FR': 'Germany',
        'Soviet Union': 'Russia',
        'Czechoslovakia': 'Czech Republic',
        'Yugoslavia': 'Serbia',
        'Dutch East Indies': 'Indonesia',
        'Irish Free State': 'Ireland'
    }
    return name_mapping.get(team_name, team_name)

def parse_score(score_string):
    """Converte string de placar para tuple de inteiros"""
    if pd.isna(score_string):
        return (0, 0)
    
    try:
        if '-' in score_string:
            home, away = score_string.split('-')
            return (int(home.strip()), int(away.strip()))
        else:
            return (0, 0)
    except:
        return (0, 0)

def calculate_match_duration(start_time, end_time):
    """Calcula duração da partida em minutos"""
    if pd.isna(start_time) or pd.isna(end_time):
        return 90  # Duração padrão
    
    try:
        start = datetime.strptime(start_time, '%H:%M')
        end = datetime.strptime(end_time, '%H:%M')
        duration = (end - start).total_seconds() / 60
        return max(90, duration)  # Mínimo 90 minutos
    except:
        return 90

def get_stage_importance(stage_name):
    """Classifica a importância da fase"""
    important_stages = ['Final', 'Semi-Final', 'Third-place match']
    group_stages = ['Group stage', 'First group stage', 'Second group stage']
    
    if stage_name in important_stages:
        return 'Alta'
    elif stage_name in group_stages:
        return 'Média'
    else:
        return 'Baixa'

def validate_match_data(match_data):
    """Valida dados de uma partida"""
    errors = []
    
    if not match_data.get('team_a.name') or not match_data.get('team_b.name'):
        errors.append("Times não especificados")
    
    if match_data.get('team_a_score') is None or match_data.get('team_b_score') is None:
        errors.append("Placar não especificado")
    
    if match_data.get('team_a.name') == match_data.get('team_b.name'):
        errors.append("Times iguais")
    
    return errors

def export_to_json(data, filename):
    """Exporta dados para JSON"""
    import json
    with open(f"docs/{filename}", 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False, default=str)

def load_country_codes():
    """Carrega códigos de países para mapas"""
    return {
        'Brazil': 'BRA', 'Germany': 'DEU', 'Italy': 'ITA', 'Argentina': 'ARG',
        'France': 'FRA', 'England': 'GBR', 'Spain': 'ESP', 'Netherlands': 'NLD',
        'Uruguay': 'URY', 'Portugal': 'PRT', 'Belgium': 'BEL', 'Croatia': 'HRV',
        'Mexico': 'MEX', 'USA': 'USA', 'Japan': 'JPN', 'South Korea': 'KOR'
    }