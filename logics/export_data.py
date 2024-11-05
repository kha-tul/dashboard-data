import streamlit as st
import pandas as pd

from logics.fetch_google_analytics_data import *
from logics.load_data import google_api_data_load
from logics.load_data import facebook_api_data_load
from logics.load_data import google_analytics_data_load
from logics.load_data import facebook_ads_data_load
from logics.load_data import instagram_data_load
from logics.utilis import load_google_api
from logics.utilis import facebook_apis_tokens
from logics.date_range import date_range_for_ads

# Correct way to access tokens from secrets.toml
user_access_token = st.secrets.access_tokens.user_access_token
page_access_token = st.secrets.access_tokens.page_access_token
page_id = st.secrets.facebook.page_id
instagram_user_id = st.secrets.instagram.instagram_user_id
adaccount_id = st.secrets.adaccount.adaccount_id

def export_data():
    # Get date range
    start_date, end_date = date_range_for_ads()
    
    # Load data from different sources
    google_api_data = google_api_data_load()
    facebook_api_data = facebook_api_data_load(user_access_token, page_id, start_date, end_date)
    google_analytics_data = google_analytics_data_load()
    facebook_ads_data = facebook_ads_data_load(user_access_token, adaccount_id, start_date, end_date)
    instagram_data = instagram_data_load(user_access_token, instagram_user_id, start_date, end_date)
    
    # Create Excel writer object
    writer = pd.ExcelWriter('./Export/Export_Data.xlsx', engine='xlsxwriter')
    
    # Export each dataset to different sheets
    if google_api_data is not None:
        google_api_data.to_excel(writer, sheet_name='Google API Data', index=False)
    
    if facebook_api_data is not None:
        facebook_api_data.to_excel(writer, sheet_name='Facebook API Data', index=False)
    
    if google_analytics_data is not None:
        google_analytics_data.to_excel(writer, sheet_name='Google Analytics Data', index=False)
    
    if facebook_ads_data is not None:
        facebook_ads_data.to_excel(writer, sheet_name='Facebook Ads Data', index=False)
    
    if instagram_data is not None:
        instagram_data.to_excel(writer, sheet_name='Instagram Data', index=False)
    
    # Save the Excel file
    writer.close()
    
    return True
