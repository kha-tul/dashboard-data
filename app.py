import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import json

# Configuração da página
st.set_page_config(
    page_title="Facebook Insights Dashboard",
    page_icon="📊",
    layout="wide"
)

# Estilo CSS personalizado
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
    }
    </style>
""", unsafe_allow_html=True)

# Função para obter insights do Facebook
def get_page_insights(page_id, access_token, since_date, until_date):
    base_url = f"https://graph.facebook.com/v20.0/{page_id}/insights"
    
    metrics = [
        "page_total_actions",
        "page_views_total",
        "page_fan_adds",
        "page_fan_removes",
        "page_impressions",
        "page_impressions_unique",
        "page_engaged_users",
        "page_posts_impressions",
        "page_posts_impressions_unique",
        "page_posts_engaged_users"
    ]
    
    params = {
        'metric': metrics,
        'access_token': access_token,
        'period': 'day',
        'since': since_date,
        'until': until_date
    }
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise an exception for bad status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching data from Facebook API: {str(e)}")
        return None

# Função para processar dados dos insights
def process_insights_data(insights_data):
    if not insights_data or 'data' not in insights_data:
        return None
    
    processed_data = {}
    for metric in insights_data['data']:
        metric_name = metric['name']
        values = metric['values']
        processed_data[metric_name] = {
            'values': [value['value'] for value in values],
            'dates': [value['end_time'] for value in values]
        }
    
    return processed_data

# Função para criar gráficos
def create_metric_chart(data, metric_name, title):
    if not data or metric_name not in data:
        return None
    
    df = pd.DataFrame({
        'Date': pd.to_datetime(data[metric_name]['dates']),
        'Value': data[metric_name]['values']
    })
    
    fig = px.line(df, x='Date', y='Value', title=title)
    fig.update_layout(
        xaxis_title="Data",
        yaxis_title="Valor",
        showlegend=False
    )
    return fig

# Título principal
st.title("📊 Facebook Page Insights Dashboard")
st.markdown("---")

# Sidebar com controles
st.sidebar.title("Configurações")

# Date range selector
col1, col2 = st.sidebar.columns(2)
with col1:
    start_date = st.date_input(
        "Data Inicial",
        datetime.now() - timedelta(days=30)
    )
with col2:
    end_date = st.date_input(
        "Data Final",
        datetime.now()
    )

# Carregar credenciais
try:
    page_id = st.secrets["facebook"]["page_id"]
    access_token = st.secrets["access_tokens"]["page_access_token"]
except Exception as e:
    st.error("Erro ao carregar as credenciais. Verifique o arquivo secrets.toml")
    st.stop()

# Botão para atualizar dados
if st.sidebar.button("Atualizar Dados"):
    with st.spinner("Carregando dados..."):
        # Fetch insights data
        insights_data = get_page_insights(
            page_id,
            access_token,
            start_date.strftime('%Y-%m-%d'),
            end_date.strftime('%Y-%m-%d')
        )
        
        if insights_data:
            # Process data
            processed_data = process_insights_data(insights_data)
            
            if processed_data:
                # Create metrics layout
                st.subheader("Métricas Principais")
                metrics_cols = st.columns(3)
                
                # Display main metrics
                metric_mappings = {
                    'page_total_actions': 'Total de Ações',
                    'page_views_total': 'Visualizações Totais',
                    'page_engaged_users': 'Usuários Engajados'
                }
                
                for i, (metric, title) in enumerate(metric_mappings.items()):
                    if metric in processed_data:
                        latest_value = processed_data[metric]['values'][-1]
                        metrics_cols[i].metric(title, latest_value)
                
                # Create charts
                st.markdown("---")
                st.subheader("Análise Temporal")
                
                # Create two columns for charts
                chart_cols = st.columns(2)
                
                # Display charts in columns
                charts_config = [
                    ('page_impressions', 'Impressões da Página'),
                    ('page_engaged_users', 'Usuários Engajados'),
                    ('page_fan_adds', 'Novos Fãs'),
                    ('page_views_total', 'Visualizações Totais')
                ]
                
                for i, (metric, title) in enumerate(charts_config):
                    col_idx = i % 2
                    with chart_cols[col_idx]:
                        chart = create_metric_chart(processed_data, metric, title)
                        if chart:
                            st.plotly_chart(chart, use_container_width=True)
                
                # Save processed data to session state
                st.session_state['processed_data'] = processed_data
            else:
                st.error("Erro ao processar os dados")
        else:
            st.error("Não foi possível obter os dados do Facebook")

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center'>
        Dashboard atualizado com métricas válidas da API v20.0 do Facebook
    </div>
""", unsafe_allow_html=True)
