import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta

def get_page_insights(page_id, start_date, end_date):
    access_token = st.secrets.access_tokens.page_access_token
    
    page_metrics = [
        'page_post_engagements',
        'page_impressions',
        'page_impressions_unique',
        'page_fans',
        'page_daily_follows',
        'page_views_total',
        'page_actions_post_reactions_total',
        'page_posts_impressions',
        'page_posts_impressions_unique',
        'page_engaged_users',
        'page_consumptions',
        'page_consumptions_unique',
        'page_negative_feedback',
        'page_negative_feedback_unique',
        'page_fan_adds_unique',
        'page_fan_removes_unique'
    ]
    
    url = f"https://graph.facebook.com/v18.0/{page_id}/insights"
    
    params = {
        'access_token': access_token,
        'metric': ','.join(page_metrics),
        'period': 'day',
        'since': start_date,
        'until': end_date
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json().get('data', [])
        
        if not data:
            st.error("No data received from Facebook API")
            return None
            
        # Process the data
        processed_data = []
        for metric in data:
            metric_name = metric['name']
            for value in metric['values']:
                processed_data.append({
                    'date': value['end_time'][:10],
                    'metric': metric_name,
                    'value': value['value']
                })
        
        # Convert to DataFrame
        df = pd.DataFrame(processed_data)
        df = df.pivot(index='date', columns='metric', values='value').reset_index()
        return df
        
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching Facebook data: {str(e)}")
        return None
