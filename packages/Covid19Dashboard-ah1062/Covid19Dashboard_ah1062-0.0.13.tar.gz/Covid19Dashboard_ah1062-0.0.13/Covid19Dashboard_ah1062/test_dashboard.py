from Covid19Dashboard_ah1062.dashboard import update_covid
from Covid19Dashboard_ah1062.dashboard import update_news

def test_update_covid():
    x, y = update_covid("Exeter", "ltla")

    assert isinstance(x, tuple) == True
    assert isinstance(y, tuple) == True

def test_update_news():
    x = []
    news = update_news(x)

    assert len(news) > 1 == True 
    assert isinstance(news[0], dict) == True
    