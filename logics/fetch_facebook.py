from facebook_business.adobjects.page import Page

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
                'metric': [metric],
                'since': start_date,
                'until': end_date,
                'period': 'day'
            })

            if insights and isinstance(insights, list) and len(insights) > 0:
                valid_metrics.append(metric)
                insights_data[metric] = insights  # Armazenar insights válidos
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
    page_id = '1060285064080786'  # Substitua pelo ID da sua página
    start_date = '2024-10-26'
    end_date = '2024-11-05'

    insights = get_page_insights(page_id, start_date, end_date)
    
    if insights:
        for metric, data in insights.items():
            print(f"Insights para {metric}: {data}")  # Exibir dados de cada métrica
    else:
        print("Não foi possível obter os insights.")
