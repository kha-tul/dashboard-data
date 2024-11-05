from facebook_business.adobjects.page import Page
from facebook_business.api import FacebookAdsApi

def get_page_insights(page_id, start_date, end_date):
    page = Page(page_id)
    
    # Lista de métricas válidas
    metrics = [
        'page_post_engagements',
        'page_impressions',
        'page_impressions_unique',
        'page_fans',
        'page_daily_follows',
        'page_views_total',
        'page_impressions_viral',
        'page_fan_adds_by_paid_non_paid_unique',
        'page_daily_follows_unique',
        'page_daily_unfollows_unique',
        'page_impressions_paid',
        'page_actions_post_reactions_total',
        'page_fans_country',
        'page_fan_adds',
        'page_fan_removes',
    ]

    valid_metrics = []
    insights_data = {}

    for metric in metrics:
        try:
            insights = page.get_insights(params={
                'metric': metric,  # Passa a métrica diretamente como string
                'since': start_date,
                'until': end_date,
                'period': 'day'
            })

            # Verifica se a resposta não é None e tem dados
            if insights and isinstance(insights, list) and len(insights) > 0:
                valid_metrics.append(metric)
                insights_data[metric] = insights  # Armazena insights válidos
            else:
                print(f"Nenhum resultado para a métrica: {metric}")
        except Exception as e:
            print(f"Erro ao obter insights para a métrica {metric}: {e}")

    if valid_metrics:
        print(f"Métricas válidas encontradas: {', '.join(valid_metrics)}")
        return insights_data  # Retorna dados acumulados
    else:
        print("Nenhuma métrica válida encontrada.")
        return None

# Exemplo de uso
if __name__ == "__main__":
    # Configure sua API do Facebook
    app_id = 'SEU_APP_ID'
    app_secret = 'SEU_APP_SECRET'
    access_token = 'SEU_ACCESS_TOKEN'
    FacebookAdsApi.init(app_id, app_secret, access_token)

    page_id = '1060285064080786'  # Substitua pelo ID da sua página
    start_date = '2024-10-26'
    end_date = '2024-11-05'

    insights = get_page_insights(page_id, start_date, end_date)
    
    if insights:
        for metric, data in insights.items():
            print(f"Insights para {metric}: {data}")  # Exibir dados de cada métrica
    else:
        print("Não foi possível obter os insights.")
