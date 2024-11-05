import streamlit as st
import pandas as pd
from facebook_business.api import FacebookAdsApi

from logics.fetch_facebook import *
from logics.date_range import *
from plots.plots_facebook import *
from plots.cards import *
from plots.plots_ads_account import *
from logics.fetch_adaccounts import *
from logics.load_data import facebook_api_data_load
from logics.load_data import facebook_ads_data_load
from logics.utilis import facebook_apis_tokens
from logics.export_data import export_data

# Configuração do sidebar
st.sidebar.page_link("main.py", label="Overview", icon="🏠")
st.sidebar.page_link("pages/Google_Ads_Performance.py", label="Google", icon="👥", disabled=False)
st.sidebar.page_link("pages/facebook_ads.py", label="Facebook", icon="👥", disabled=False)
st.sidebar.page_link("pages/instagram_data.py", label="Instagram", icon="👥", disabled=False)

# Obtenção dos tokens e IDs
(page_access_token, user_access_token, page_id, adaccount_account_id, adaccount_id) = facebook_apis_tokens()

# Inicialização da API do Facebook
FacebookAdsApi.init(access_token=page_access_token)

st.sidebar.divider()
start_date, end_date = date_range()
selected_range = date_range_for_ads()

export_button = st.sidebar.toggle("Export_Data")
if export_button:
    export_data(start_date, end_date)

try:
    # Carregar dados de insights da página
    (page_insights, dates, page_post_engagements, page_impressions, page_impressions_unique,
     page_fans, unique_page_fan, page_follows, page_views,
     page_negative_feedback_unique, page_impressions_viral,
     page_fan_adds_by_paid_non_paid_unique, page_daily_follows_unique,
     page_daily_unfollows_unique, page_impressions_by_age_gender_unique,
     page_impressions_organic_unique_v2, page_impressions_paid, post_reactions,
     page_fans_country, page_fan_adds, page_fan_removes) = facebook_api_data_load(page_id, start_date, end_date)

    # Carregar dados de anúncios
    ads_insights_, ada_account = facebook_ads_data_load(user_access_token, adaccount_account_id, adaccount_id, selected_range)
    ads_insights = pd.DataFrame(ads_insights_)

    # Agrupando detalhes dos anúncios
    group_ads_details = group_by_ad_name(ads_insights)
    group_ads_details['roi'] = round((group_ads_details['conversions'] / group_ads_details['spend']) * 100, 2)
    ad_names = group_ads_details['ad_name']
    roi = group_ads_details['roi']
    spend = group_ads_details['spend']
    conversions = group_ads_details['conversions']

    # Exibir cartões com dados de insights da página
    col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])
    with col1:
        cards("Total de Visualizações de Página", page_views.sum()[0] if not page_views.empty else 0)
    with col2:
        cards("Total de Seguidores", page_follows.sum()[0] if not page_follows.empty else 0)
    with col3:
        cards("Total de Curtidas", unique_page_fan)
    with col4:
        cards("Feedbacks Negativos", page_negative_feedback_unique.sum()[0] if not page_negative_feedback_unique.empty else 0)
    with col5:
        cards("Impressões Virais", page_impressions_viral.sum()[0] if not page_impressions_viral.empty else 0)

    st.divider()

    # Se houver dados de insights
    if page_insights:
        page_impression_engagement(page_post_engagements, page_impressions, page_impressions_unique, dates)

        col1, col2 = st.columns([1, 1])
        with col1:
            page_fan_adds_by_paid_unpaid_unique(page_fan_adds_by_paid_non_paid_unique, dates)
        with col2:
            page_daily_follows_unfollow(page_daily_follows_unique, page_daily_unfollows_unique, dates)

        try:
            col1, col2 = st.columns([1, 1])
            with col1:
                page_impressions_by_age_gender_male(page_impressions_by_age_gender_unique, dates)
            with col2:
                page_impressions_by_age_gender_female(page_impressions_by_age_gender_unique, dates)
        except Exception as age_gender_error:
            st.warning(f"Error processing age/gender insights: {age_gender_error}")

        page_impressions_organic_paid(page_impressions_organic_unique_v2, page_impressions_paid, dates)
        st.divider()

        col1, col2 = st.columns([1, 1])
        with col1:
            page_fans_country_plot(page_fans_country, dates)
        with col2:
            page_actions_post_reactions(post_reactions, dates)

        page_fan_adds_remove(page_fan_adds, page_fan_removes, dates)

        st.divider()

        try:
            cpm_cpp_ctr_clicks(group_ads_details)
            spend_on_ads(group_ads_details)

            col1, col2 = st.columns([1, 1])
            with col1:
                roi_by_ad_names(ad_names, roi)
            with col2:
                total_roi_spend_conv_pie_charts(roi, spend, conversions)

            ads_stacked_bar_chart(ad_names, roi, spend, conversions, selected_range)
        except Exception as ad_error:
            st.warning(f"Error processing ads insights: {ad_error}")

    else:
        st.write("No insights data available")

except Exception as e:
    st.error(f"Error fetching page insights: {e}")
