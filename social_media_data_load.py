import pandas as pd
import requests
from datetime import datetime, timedelta
import json

def get_access_token():
    """Get access token from environment or configuration"""
    return "YOUR_ACCESS_TOKEN_HERE"

def facebook_data_load():
    """
    Facebook data loading function for API v20.0
    """
    # Format dates
    end_date = datetime.now()
    start_date = end_date - timedelta(days=10)
    
    since = start_date.strftime('%Y-%m-%d')
    until = end_date.strftime('%Y-%m-%d')
    
    # Credentials
    page_id = "YOUR_PAGE_ID"
    access_token = get_access_token()
    
    # Base URL for Facebook Graph API v20.0
    base_url = "https://graph.facebook.com/v20.0"
    
    # Updated metrics based on Graph API v20.0
    metrics = [
        'page_impressions',
        'page_engaged_users',
        'page_fan_adds',
        'page_views_total'
    ]
    
    try:
        # Fetch page insights
        insights_url = f"{base_url}/{page_id}/insights"
        insights_params = {
            'metric': ','.join(metrics),
            'period': 'day',
            'since': since,
            'until': until,
            'access_token': access_token
        }
        
        insights_response = requests.get(insights_url, params=insights_params)
        insights_response.raise_for_status()
        insights_data = insights_response.json()
        
        # Process insights data
        processed_data = []
        for metric in insights_data.get('data', []):
            metric_name = metric['name']
            for value in metric['values']:
                processed_data.append({
                    'date': value['end_time'][:10],
                    'metric': metric_name,
                    'value': value['value']
                })
        
        # Convert to DataFrame
        insights_df = pd.DataFrame(processed_data)
        
        # Save insights data
        insights_df.to_csv('facebook_insights.csv', index=False)
        
        # Fetch posts data
        posts_url = f"{base_url}/{page_id}/posts"
        posts_params = {
            'fields': 'id,message,created_time,likes.summary(true),comments.summary(true),shares',
            'since': since,
            'until': until,
            'access_token': access_token
        }
        
        posts_response = requests.get(posts_url, params=posts_params)
        posts_response.raise_for_status()
        posts_data = posts_response.json()
        
        # Process posts data
        posts_processed = []
        for post in posts_data.get('data', []):
            post_data = {
                'post_id': post['id'],
                'created_time': post['created_time'][:10],
                'message': post.get('message', ''),
                'likes': post.get('likes', {}).get('summary', {}).get('total_count', 0),
                'comments': post.get('comments', {}).get('summary', {}).get('total_count', 0),
                'shares': post.get('shares', {}).get('count', 0) if 'shares' in post else 0
            }
            posts_processed.append(post_data)
        
        posts_df = pd.DataFrame(posts_processed)
        posts_df.to_csv('facebook_posts.csv', index=False)
        
        return insights_df, posts_df
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching Facebook data: {str(e)}")
        return None, None

def instagram_data_load():
    """
    Instagram data loading function for API v20.0
    """
    # Format dates
    end_date = datetime.now()
    start_date = end_date - timedelta(days=10)
    
    since = start_date.strftime('%Y-%m-%d')
    until = end_date.strftime('%Y-%m-%d')
    
    # Credentials
    instagram_account_id = "YOUR_INSTAGRAM_ACCOUNT_ID"
    access_token = get_access_token()
    
    # Base URL for Instagram Graph API v20.0
    base_url = "https://graph.facebook.com/v20.0"
    
    try:
        # Updated metrics based on Instagram Insights API
        metrics = [
            'reach',
            'impressions',
            'profile_views'
        ]
        
        insights_url = f"{base_url}/{instagram_account_id}/insights"
        insights_params = {
            'metric': ','.join(metrics),
            'period': 'day',
            'since': since,
            'until': until,
            'access_token': access_token
        }
        
        insights_response = requests.get(insights_url, params=insights_params)
        insights_response.raise_for_status()
        insights_data = insights_response.json()
        
        # Process insights data
        processed_data = []
        for metric in insights_data.get('data', []):
            metric_name = metric['name']
            for value in metric['values']:
                processed_data.append({
                    'date': value['end_time'][:10],
                    'metric': metric_name,
                    'value': value['value']
                })
        
        insights_df = pd.DataFrame(processed_data)
        insights_df.to_csv('instagram_insights.csv', index=False)
        
        # Fetch media data
        media_url = f"{base_url}/{instagram_account_id}/media"
        media_params = {
            'fields': 'id,caption,media_type,timestamp,like_count,comments_count',
            'since': since,
            'until': until,
            'access_token': access_token
        }
        
        media_response = requests.get(media_url, params=media_params)
        media_response.raise_for_status()
        media_data = media_response.json()
        
        # Process media data
        media_processed = []
        for media in media_data.get('data', []):
            media_item = {
                'media_id': media['id'],
                'timestamp': media['timestamp'][:10],
                'media_type': media.get('media_type', ''),
                'caption': media.get('caption', ''),
                'like_count': media.get('like_count', 0),
                'comments_count': media.get('comments_count', 0)
            }
            media_processed.append(media_item)
        
        media_df = pd.DataFrame(media_processed)
        media_df.to_csv('instagram_media.csv', index=False)
        
        return insights_df, media_df
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching Instagram data: {str(e)}")
        return None, None

if __name__ == "__main__":
    # Test Facebook data load
    fb_insights, fb_posts = facebook_data_load()
    if fb_insights is not None and fb_posts is not None:
        print("Facebook data loaded successfully")
        print("
Facebook Insights Preview:")
        print(fb_insights.head())
        print("
Facebook Posts Preview:")
        print(fb_posts.head())
    
    # Test Instagram data load
    ig_insights, ig_media = instagram_data_load()
    if ig_insights is not None and ig_media is not None:
        print("
Instagram data loaded successfully")
        print("
Instagram Insights Preview:")
        print(ig_insights.head())
        print("
Instagram Media Preview:")
        print(ig_media.head())
