import datetime
from conftest import BASE_URL, client


def test_financial_data_endpoint():
    url = BASE_URL + "/api/financial_data"
    response = client.get(url)
    assert response.status_code == 200


def test_statistics_endpoint():
    start_date = (datetime.datetime.now() - datetime.timedelta(days=7)).strftime("%Y-%m-%d")
    end_date = datetime.datetime.now().strftime("%Y-%m-%d")
    symbol = "AAPL"
    url = (
        BASE_URL
        + "/api/statistics"
        + f"?start_date={start_date}&end_date={end_date}&symbol={symbol}"
    )
    response = client.get(url)
    assert response.status_code == 200
