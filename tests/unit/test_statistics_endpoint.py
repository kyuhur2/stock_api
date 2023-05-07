import datetime
from conftest import BASE_URL, client


def test_optional_params():
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


def test_nonexistent_symbol():
    start_date = (datetime.datetime.now() - datetime.timedelta(days=7)).strftime("%Y-%m-%d")
    end_date = datetime.datetime.now().strftime("%Y-%m-%d")
    symbol = "MSFT"
    endpoint = "/api/statistics"
    url = BASE_URL + endpoint + f"?start_date={start_date}&end_date={end_date}&symbol={symbol}"
    response = client.get(url)
    assert response.status_code == 404
