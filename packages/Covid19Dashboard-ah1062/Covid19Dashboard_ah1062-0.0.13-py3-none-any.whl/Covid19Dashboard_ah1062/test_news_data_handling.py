from Covid19Dashboard_ah1062.covid_news_handling import news_API_request
from Covid19Dashboard_ah1062.covid_news_handling import get_news_data

def test_news_API_request():
    assert news_API_request()
    assert news_API_request('Covid COVID-19 coronavirus') == news_API_request()

def test_get_news_data():
    data = get_news_data()
    assert isinstance(data, list)
