import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta

def fetch_instagram_insights(user_id, start_date, end_date, metrics, period='day'):
    access_token = st.secrets.access_tokens.user_access_token
    url = f"https://graph.facebook.com/v18.0/{user_id}/insights"
    
    params = {
        'access_token': access_token,
        'metric': ','.join(metrics),
        'period': period,
        'since': start_date,
        'until': end_date
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json().get('data', [])
        
        if not data:
            st.error("No data received from Instagram API")
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
        st.error(f"Error fetching Instagram data: {str(e)}")
        return None

def get_instagram_insights(instagram_user_id, start_date, end_date):
    metrics = [
        'impressions',
        'reach',
        'profile_views',
        'follower_count',
        'email_contacts',
        'get_directions_clicks',
        'phone_call_clicks',
        'text_message_clicks',
        'website_clicks'
    ]
    
    return fetch_instagram_insights(instagram_user_id, start_date, end_date, metrics)
