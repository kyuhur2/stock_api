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


def test_incorrect_symbol_1():
    symbol = "MSFT"
    start_date = (datetime.datetime.now() - datetime.timedelta(days=7)).strftime("%Y-%m-%d")
    end_date = datetime.datetime.now().strftime("%Y-%m-%d")
    endpoint = "/api/statistics"
    url = BASE_URL + endpoint + f"?start_date={start_date}&end_date={end_date}&symbol={symbol}"
    response = client.get(url)
    assert response.status_code == 404


def test_incorrect_symbol_2():
    symbol = "SDFJLSADFSALFD"
    start_date = (datetime.datetime.now() - datetime.timedelta(days=7)).strftime("%Y-%m-%d")
    end_date = datetime.datetime.now().strftime("%Y-%m-%d")
    endpoint = "/api/statistics"
    url = BASE_URL + endpoint + f"?start_date={start_date}&end_date={end_date}&symbol={symbol}"
    response = client.get(url)
    assert response.status_code == 400


def test_incorrect_symbol_3():
    symbol = "-11111111111"
    start_date = (datetime.datetime.now() - datetime.timedelta(days=7)).strftime("%Y-%m-%d")
    end_date = datetime.datetime.now().strftime("%Y-%m-%d")
    endpoint = "/api/statistics"
    url = BASE_URL + endpoint + f"?start_date={start_date}&end_date={end_date}&symbol={symbol}"
    response = client.get(url)
    assert response.status_code == 400


def test_incorrect_date_format():
    start_date = (datetime.datetime.now() - datetime.timedelta(days=7)).strftime("%m-%d-%Y")
    end_date = datetime.datetime.now().strftime("%m-%d-%Y")
    symbol = "AAPL"
    url = (
        BASE_URL
        + "/api/financial_data"
        + f"?start_date={start_date}&end_date={end_date}&symbol={symbol}"
    )
    response = client.get(url)
    assert response.status_code == 400


def test_incorrect_date_type():
    start_date = 20230501
    end_date = datetime.datetime.now().strftime("%m-%d-%Y")
    symbol = "AAPL"
    url = (
        BASE_URL
        + "/api/financial_data"
        + f"?start_date={start_date}&end_date={end_date}&symbol={symbol}"
    )
    response = client.get(url)
    assert response.status_code == 400
