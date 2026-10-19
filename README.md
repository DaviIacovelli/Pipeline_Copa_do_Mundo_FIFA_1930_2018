# 🏆 Análise da Copa do Mundo FIFA

Sistema completo de análise de dados históricos da Copa do Mundo FIFA utilizando Python, MongoDB e Plotly.

## 📊 Sobre o Projeto

Este projeto realiza uma análise estatística completa das edições da Copa do Mundo FIFA desde 1930 até 2018, incluindo:

- 📈 Estatísticas históricas de todas as edições
- ⚽ Desempenho de seleções ao longo do tempo
- 🏆 Análise de partidas memoráveis e finais
- 📊 Visualizações interativas e relatórios
- 💾 Pipeline completo de ETL (Extract, Transform, Load)

## 🚀 Funcionalidades

### 🔍 Análises Realizadas

- **Estatísticas por Edição**: Gols, partidas, média de gols por jogo
- **Desempenho por Time**: Vitórias, derrotas, gols marcados/sofridos
- **Análise por Fase**: Grupo, oitavas, quartas, semi e final
- **Confrontos Diretos**: Histórico entre seleções rivais
- **Partidas Memoráveis**: Jogos com maior número de gols
- **Linha do Tempo**: Evolução do futebol através dos anos

### 📈 Visualizações

- Gráficos interativos com Plotly
- Dashboards completos
- Mapas de campeões mundiais
- Análises comparativas entre seleções
- Exportação em HTML e PNG

### 💾 Gerenciamento de Dados

- Pipeline ETL automatizado
- Backup automático do MongoDB
- Armazenamento de dados processados
- Limpeza inteligente de arquivos antigos

## 🛠️ Tecnologias Utilizadas

- **Python 3.8+**
- **MongoDB** (Atlas ou Local)
- **Pandas** - Manipulação de dados
- **Plotly** - Visualizações interativas
- **PyMongo** - Conexão com MongoDB
- **Python-dotenv** - Gerenciamento de configurações

## 📁 Estrutura do Projeto

```
Copa_Do_Mundo_FIFA/
├── 📄 main.py                 # Script principal
├── 📄 manage_data.py          # Gerenciador de dados
├── 📄 requirements.txt        # Dependências
├── 📄 .env                   # Variáveis de ambiente
├── 📂 data/
│   ├── 📂 raw/               # Dados originais (CSV)
│   ├── 📂 processed/         # Dados processados
│   └── 📂 database/          # Backups do MongoDB
├── 📂 docs/
│   └── 📂 imagens/           # Gráficos e visualizações
├── 📂 src/
│   ├── 📂 database/          # Configuração do MongoDB
│   ├── 📂 etl/               # Pipeline de dados
│   ├── 📂 analysis/          # Análises estatísticas
│   ├── 📂 visualization/     # Geração de gráficos
│   └── 📂 utils/             # Utilitários e configurações
└── 📂 tests/                 # Testes unitários
```

## ⚡ Instalação e Configuração

### 1. Clone o repositório

```bash
git clone <url-do-repositorio>
cd Copa_Do_Mundo_FIFA
```

### 2. Configure o ambiente virtual

```bash
# Criar ambiente virtual
python -m venv venv

# Ativar no Windows
venv\Scripts\activate

# Ativar no Linux/Mac
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt

# Instalação adicional para MongoDB Atlas
python -m pip install "pymongo[srv]"
```

### 4. Configure as variáveis de ambiente

Crie o arquivo `.env` na raiz do projeto:

```env
# Para MongoDB Local (padrão)
MONGODB_URI=mongodb://localhost:27017/
MONGODB_DB_NAME=fifa_worldcup_analysis

# Para MongoDB Atlas (Cloud)
# MONGODB_URI=mongodb+srv://usuario:senha@cluster.mongodb.net/
# MONGODB_DB_NAME=fifa_worldcup_analysis

DEBUG_MODE=True
```

### 5. Prepare os dados

Coloque o arquivo `world_fifa_worldcup_matches.csv` na pasta `data/raw/`

## 🎯 Como Usar

### Executar Análise Completa

```bash
python main.py
```

### Gerenciar Dados

```bash
python manage_data.py
```

### Executar Testes

```bash
python -m pytest tests/ -v
```

### Opções do Gerenciador de Dados

```
1. Listar arquivos processados
2. Listar backups do banco
3. Carregar dados processados mais recentes
4. Limpar arquivos antigos
5. Verificar estrutura de pastas
6. Sair
```

## 📊 Saídas Geradas

### 🗂️ Dados Processados (`data/processed/`)

- `worldcup_matches_processed_*.csv` - Dados limpos e transformados
- `*_analysis_*.json` - Resultados das análises
- `processing_metadata_*.json` - Metadados do processamento

### 📦 Backups (`data/database/`)

- `backup_*/matches_backup.json` - Backup completo do MongoDB
- `backup_*/backup_stats.json` - Estatísticas do backup

### 📈 Visualizações (`docs/imagens/`)

- `*.html` - Gráficos interativos
- `*.png` - Imagens estáticas para relatórios

### 📋 Principais Gráficos

- Evolução de gols por edição
- Desempenho por fase da competição
- Análise de seleções específicas
- Confrontos diretos entre times
- Mapas de campeões mundiais

## 🔧 Configuração do MongoDB

### Opção 1: MongoDB Local

1. Instale o [MongoDB Community Edition](https://www.mongodb.com/try/download/community)
2. Inicie o serviço MongoDB
3. Use a URI: `mongodb://localhost:27017/`

### Opção 2: MongoDB Atlas (Cloud)

1. Crie uma conta em [MongoDB Atlas](https://www.mongodb.com/atlas)
2. Crie um cluster gratuito
3. Adicione seu IP à whitelist
4. Crie um usuário de banco de dados
5. Use a URI de conexão fornecida

## 🐛 Solução de Problemas

### Erro de Conexão MongoDB

```bash
# Testar conexão
python -c "from src.utils.config import Config; Config.test_connection()"
```

### Dependências Ausentes

```bash
# Reinstalar dependências
pip install --upgrade -r requirements.txt
```

### Problemas de Importação

```bash
# Verificar estrutura de pastas
python manage_data.py
# Escolher opção 5 (Verificar estrutura de pastas)
```

## 📈 Exemplos de Análise

### Estatísticas por Edição

```python
from src.analysis.tournament_analysis import TournamentAnalyzer

analyzer = TournamentAnalyzer()
summary = analyzer.get_tournament_summary()

for edition in summary:
    print(f"{edition['_id']}: {edition['total_matches']} jogos, "
          f"{edition['total_goals']} gols")
```

### Desempenho de um Time

```python
team_stats = analyzer.get_team_performance('Brazil')
print(f"Brasil: {team_stats['wins']} vitórias em {team_stats['total_matches']} jogos")
```

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto é para fins educacionais. Os dados são baseados em dataset público da Copa do Mundo FIFA.

## 👥 Autores

- **Davi Iacovelli** - [DaviIacovelli](https://github.com/DaviIacovelli)

## 🙋‍♂️ Suporte

Em caso de problemas:

1. Verifique se todas as dependências estão instaladas
2. Confirme que o MongoDB está rodando
3. Verifique o arquivo `.env` está configurado corretamente
4. Execute `python manage_data.py` para diagnosticar problemas

---

**⭐ Se este projeto foi útil, deixe uma estrela no repositório!**
