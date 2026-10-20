# ⚽ Football Analytics Hub

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35%2B-FF4B4B.svg?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Plotly](https://img.shields.io/badge/Plotly-5.22%2B-3F4F75.svg?logo=plotly&logoColor=white)](https://plotly.com/)
[![Pandas](https://img.shields.io/badge/Pandas-2.2%2B-150458.svg?logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Tests: 18 Passed](https://img.shields.io/badge/Tests-18%20Passed-brightgreen.svg)]()

> Plataforma completa de análise de dados, inteligência esportiva e Business Intelligence do futebol baseada em dados reais, construída em Python e Streamlit.

---

## 📌 Visão Geral do Projeto

O **Football Analytics Hub** é uma aplicação web moderna voltada para entusiastas, analistas de desempenho e profissionais de Business Intelligence no esporte. A plataforma consome dados ao vivo de competições mundiais via API oficial, processa indicadores estatísticos e os apresenta através de dashboards interativos, matrizes de dispersão, gráficos de radar e tabelas estilizadas.

### 🎯 Diferenciais de Engenharia e Arquitetura:
1. **Separação Rigorosa de Dados**:
   - Suporte a dados ao vivo via API oficial com indicação explícita da fonte.
   - Modo Demonstração (*Offline*) de alta fidelidade para testes sem credenciais, com alerta visual claro e sem misturar silenciosamente dados simulados com reais.
2. **Resiliência e Controle de Rate Limit (HTTP 429)**:
   - Respeito estrito aos limites da API (`Retry-After`), evitando requisições em loop ou bloqueios de IP.
   - Cache de contingência (*stale-while-revalidate*): se a rede ou a API oscilarem, a aplicação preserva e exibe com transparência os últimos dados válidos conhecidos.
3. **Regras de Classificação Específicas por Liga**:
   - As zonas continentais (Libertadores, Champions League, Europa League, Sul-Americana) e rebaixamentos respeitam o regulamento exato de cada campeonato e temporada (ex: Z-4 no Brasileirão com G-4/G-6, G-4 e Z-3 na Premier League, Play-offs na Bundesliga).

---

## 🚀 Funcionalidades

### 🏠 Visão Geral da Temporada (Dashboard Executivo)
- Indicadores macro: Total de jogos, gols marcados, média por partida e aproveitamento do líder.
- Donut chart da distribuição de resultados (Vitória Mandante x Empates x Visitante).
- Matriz de dispersão: Gols Pró x Gols Contra (quadrantes de eficiência ofensiva e defensiva).
- Insights automáticos orientados a dados (disputa de título, melhor ataque, solidez defensiva, fator casa).

### 🏆 Campeonatos & Classificação
- Tabela completa de pontuação, jogos, vitórias, empates, derrotas, saldo e aproveitamento percentual.
- Visualização de forma recente dos últimos 5 jogos com badges coloridos (🟩 V, 🟨 E, 🟥 D).
- Zonas de classificação identificadas por cores e badges específicos de cada liga.
- Filtros interativos por zona e busca por clube.
- Comparador rápido entre duas equipes da competição.

### 🛡️ Raio-X das Equipes
- Perfil detalhado de cada clube com escudo oficial e dados cadastrais.
- Desempenho desdobrado: Geral vs Mandante (Casa) vs Visitante (Fora).
- Radar esportivo de eficiência técnica (Poder Ofensivo, Solidez Defensiva, Fator Mandante, Eficiência Fora, Consistência).
- Comparador de Confronto Direto (*Head-to-Head*) com histórico de embates na temporada.

### 🎯 Artilharia & Atletas
- Ranking dos maiores goleadores com estatísticas reais fornecidas pela API (gols, assistências, pênaltis, média de gols por jogo).
- Gráfico de barras com volume de participações em gols.
- Comparativo direto individual entre dois artilheiros.

### 📅 Calendário de Jogos
- Consulta completa de partidas anteriores com placares e confrontos futuros agendados.
- Filtros por rodada, status (Finalizadas, Agendadas, Ao Vivo) e busca por clube.

### 🔬 Business Intelligence & Análise Avançada
- Fator Mandante da competição e razão de vantagem local.
- Métricas empíricas de volume de gols: frequência de Mais de 1.5, 2.5 e 3.5 gols.
- Taxa de Ambos Marcam (BTTS) e frequência de *Clean Sheets*.
- Rankings de eficiência (maior média de gols/jogo e defesas menos vazadas).

---

## 🏗️ Arquitetura do Projeto

```
football-analytics-hub/
├── .streamlit/
│   ├── config.toml               # Tema esportivo escuro, layout e estilos
│   └── secrets.toml.example      # Modelo para configuração de chaves na nuvem
├── src/
│   ├── api/
│   │   ├── client.py             # Cliente HTTP, controle de rate limit (429) e cache
│   │   ├── mock_data.py          # Conjunto de demonstração sintético (BSA e PL)
│   │   └── models.py             # Dataclasses tipadas (StandingRow, Match, Scorer)
│   ├── analytics/
│   │   ├── standings.py          # Tratamento de tabelas, PPG e aproveitamento
│   │   ├── matches.py            # Fator casa, médias de gols, BTTS, Over/Under
│   │   ├── teams.py              # Registros mandante/visitante, radar e Head-to-Head
│   │   └── insights.py           # Geração automática de insights analíticos
│   ├── components/
│   │   ├── cards.py              # Cards modernos de KPI e banners de status
│   │   ├── charts.py             # Visualizações Plotly (Donut, Scatter, Radar, Barras)
│   │   └── tables.py             # Tabelas HTML customizadas com escudos e zonas
│   ├── utils/
│   │   ├── config.py             # Metadados e regras de zonas de cada liga
│   │   └── formatting.py         # Formatação pt-BR de datas, percentuais e status
│   └── views/
│       ├── dashboard.py          # Visão Geral da temporada
│       ├── competitions.py       # Tabela e classificação
│       ├── teams.py              # Raio-X e comparador de clubes
│       ├── players.py            # Artilharia e atletas
│       ├── matches.py            # Calendário de partidas
│       └── advanced_analytics.py # BI e métricas estatísticas avançadas
├── tests/
│   ├── test_analytics.py         # Testes de regras de negócio e cálculos
│   ├── test_api_client.py        # Testes de cliente de API, demo mode e rate limit
│   └── test_formatting.py        # Testes de utilitários e zonas de campeonato
├── app.py                        # Ponto de entrada Streamlit (navegação e layout)
├── requirements.txt              # Dependências do projeto
├── .env.example                  # Template de variáveis de ambiente
├── .gitignore                    # Regras de exclusão do Git
├── LICENSE                       # Licença MIT e atribuição da API
└── README.md                     # Documentação completa
```

---

## ⚙️ Instalação e Execução Local

### Pré-requisitos
- Python 3.10 ou superior instalado.
- Gerenciador de pacotes `pip`.

### 1. Clonar ou Acessar o Diretório
```bash
cd football-analytics-hub
```

### 2. Criar e Ativar Ambiente Virtual (Recomendado)
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar Dependências
```bash
pip install -r requirements.txt
```

### 4. Configurar Chave de API (Opcional)
Se desejar acessar dados ao vivo pela API do **football-data.org**:
1. Obtenha uma chave gratuita em: https://www.football-data.org/client/register
2. Copie o arquivo de exemplo:
   ```bash
   cp .env.example .env
   ```
3. Insira sua chave no `.env`:
   ```ini
   FOOTBALL_DATA_API_KEY=sua_chave_aqui
   ```
> *Nota: Se você não configurar uma chave, a aplicação funcionará normalmente no **Modo Demonstração**, que pode ser ativado a qualquer momento no menu lateral.*

### 5. Executar a Aplicação
```bash
streamlit run app.py
```
Acesse no seu navegador: `http://localhost:8501`.

---

## 🧪 Executando os Testes Automatizados

O projeto possui uma suíte completa de testes unitários cobrindo o cliente de API, a camada estatística, zonas de competição e utilitários:

```bash
python -m pytest tests/ -v
```

Resultado esperado:
```
18 passed in 0.69s
```

---

## ☁️ Publicação no Streamlit Community Cloud

A aplicação está 100% pronta para publicação gratuita:

1. Suba o código para um repositório no **GitHub**.
2. Acesse [share.streamlit.io](https://share.streamlit.io/) e faça login com sua conta do GitHub.
3. Clique em **"New app"** e selecione o repositório, a branch `main` e o arquivo principal `app.py`.
4. Em **"Advanced settings..."** > **"Secrets"**, adicione sua chave de API (opcional para rodar com dados ao vivo):
   ```toml
   FOOTBALL_DATA_API_KEY = "sua_chave_real_aqui"
   ```
5. Clique em **"Deploy!"**. Sua aplicação estará online com URL pública compartilhável.

---

## ⚖️ Atribuição e Licença

- **Licença**: MIT. Consulte o arquivo [LICENSE](LICENSE) para detalhes.
- **Fonte de Dados**: Este software utiliza dados da API [football-data.org](https://www.football-data.org/). Os dados são de propriedade de seus respectivos organizadores e fornecedores.
