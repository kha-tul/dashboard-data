from facebook_business.adobjects.page import Page

def get_page_insights(page_id, start_date, end_date):
    page = Page(page_id)
    
    # Lista de métricas conhecidas
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
    
    # Lista de métricas a serem ignoradas por não serem válidas
    invalid_metrics = [
        'page_negative_feedback_unique',
        'page_impressions_by_age_gender_unique',
        'page_impressions_organic_unique_v2'
    ]
    
    # Filtrar métricas conhecidas para evitar chamadas inválidas
    valid_metrics = []
    for metric in metrics:
        if metric not in invalid_metrics:
            try:
                # Verificar se a métrica é válida
                insights = page.get_insights(params={
                    'metric': [metric],  # Passando a métrica como uma lista
                    'since': start_date,
                    'until': end_date,
                    'period': 'day'
                })
                
                # Adiciona a métrica se retornar resultados
                if insights and isinstance(insights, list) and len(insights) > 0:
                    valid_metrics.append(metric)
            except Exception as e:
                print(f"Erro com a métrica {metric}: {e}")

    # Se todas as métricas forem válidas, faça uma chamada completa
    if valid_metrics:
        print(f"Métricas válidas encontradas: {', '.join(valid_metrics)}")
        params = {
            'metric': ','.join(valid_metrics),  # Passamos a lista de métricas válidas como uma string
            'since': start_date,
            'until': end_date,
            'period': 'day'
        }
        try:
            insights = page.get_insights(params=params)
            # Verificar se os insights retornam resultados
            if insights and isinstance(insights, list) and len(insights) > 0:
                return insights
            else:
                print("Nenhum insight retornado ou resultado inválido.")
                return None
        except Exception as e:
            print(f"Erro ao obter os insights: {e}")
            return None
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
        print(insights)
    else:
        print("Não foi possível obter os insights.")
