import datetime
from conftest import BASE_URL, client


def test_optional_params():
    symbols = ["AAPL", "IBM"]
    for symbol in symbols:
        start_date = (datetime.datetime.now() - datetime.timedelta(days=7)).strftime("%Y-%m-%d")
        end_date = datetime.datetime.now().strftime("%Y-%m-%d")
        url = (
            BASE_URL
            + "/api/financial_data"
            + f"?start_date={start_date}&end_date={end_date}&symbol={symbol}"
        )
        response = client.get(url)
        assert response.status_code == 200


def test_altered_required_params():
    page = 1
    limit = 3
    url = BASE_URL + "/api/financial_data" + f"?page={page}&limit={limit}"
    response = client.get(url)
    assert response.status_code == 200


def test_nonexistent_symbol():
    symbol = "MSFT"
    endpoint = "/api/financial_data"
    url = BASE_URL + endpoint + f"?symbol={symbol}"
    response = client.get(url)
    assert response.status_code == 404
