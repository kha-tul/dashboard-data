import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from google.oauth2 import service_account
from googleapiclient.discovery import build

from logics.fetch_instagram import get_valid_metrics_by_days
from logics.fetch_instagram import get_instagram_insights
from logics.fetch_facebook import get_page_insights

def load_google_api():
    try:
        credentials = service_account.Credentials.from_service_account_info(
            st.secrets["google"],
            scopes=['https://www.googleapis.com/auth/spreadsheets.readonly']
        )
        service = build('sheets', 'v4', credentials=credentials)
        return service
    except Exception as e:
        st.error(f"Error loading Google API: {str(e)}")
        return None

def facebook_apis_tokens():
    try:
        return {
            'user_access_token': st.secrets.access_tokens.user_access_token,
            'page_access_token': st.secrets.access_tokens.page_access_token,
            'page_id': st.secrets.facebook.page_id,
            'instagram_user_id': st.secrets.instagram.instagram_user_id,
            'adaccount_id': st.secrets.adaccount.adaccount_id
        }
    except Exception as e:
        st.error(f"Error loading Facebook API tokens: {str(e)}")
        return None

def instagram_api_data_fetch(instagram_user_id, start_date, end_date):
    try:
        return get_instagram_insights(instagram_user_id, start_date, end_date)
    except Exception as e:
        st.error(f"Error fetching Instagram data: {str(e)}")
        return None

def facebook_api_data_fetch(page_id, start_date, end_date):
    try:
        return get_page_insights(page_id, start_date, end_date)
    except Exception as e:
        st.error(f"Error fetching Facebook data: {str(e)}")
        return None
