import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

from logics.utilis import load_google_api
from logics.utilis import facebook_apis_tokens
from logics.utilis import instagram_api_data_fetch
from logics.utilis import facebook_api_data_fetch

def google_api_data_load():
    try:
        service = load_google_api()
        if not service:
            return None
            
        # Add your Google Sheets logic here
        return pd.DataFrame()  # Replace with actual data loading
    except Exception as e:
        st.error(f"Error loading Google API data: {str(e)}")
        return None

def facebook_api_data_load(access_token, page_id, start_date, end_date):
    try:
        return facebook_api_data_fetch(page_id, start_date, end_date)
    except Exception as e:
        st.error(f"Error loading Facebook API data: {str(e)}")
        return None

def google_analytics_data_load():
    try:
        # Add your Google Analytics logic here
        return pd.DataFrame()  # Replace with actual data loading
    except Exception as e:
        st.error(f"Error loading Google Analytics data: {str(e)}")
        return None

def facebook_ads_data_load(access_token, adaccount_id, start_date, end_date):
    try:
        # Add your Facebook Ads logic here
        return pd.DataFrame()  # Replace with actual data loading
    except Exception as e:
        st.error(f"Error loading Facebook Ads data: {str(e)}")
        return None

def instagram_data_load(access_token, instagram_user_id, start_date, end_date):
    try:
        return instagram_api_data_fetch(instagram_user_id, start_date, end_date)
    except Exception as e:
        st.error(f"Error loading Instagram data: {str(e)}")
        return None
