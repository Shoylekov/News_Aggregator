import requests

def fetch_news(preferences, page=1, page_size=5):
    API_KEY = 'Your API key'
    url = 'https://newsapi.org/v2/everything'
    
    topics = preferences.split(',')
    articles = []
    total_results = 0  # Default if API does not return it

    for topic in topics:
        params = {
            'q': topic.strip(),
            'apiKey': API_KEY,
            'pageSize': page_size,  # Number of articles per page
            'page': page  # Current page number
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            articles.extend(data.get('articles', []))
            total_results = data.get('totalResults', 0)  # Get total results for the query
    
    return articles, total_results
