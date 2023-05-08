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


def test_incorrect_page_limit_type_1():
    page = 1
    limit = 3.1
    url = BASE_URL + "/api/financial_data" + f"?page={page}&limit={limit}"
    response = client.get(url)
    assert response.status_code == 422


def test_incorrect_page_limit_type_2():
    page = 0.5
    limit = 3.1
    url = BASE_URL + "/api/financial_data" + f"?page={page}&limit={limit}"
    response = client.get(url)
    assert response.status_code == 422


def test_incorrect_page_limit_type_3():
    page = -1
    limit = 5
    url = BASE_URL + "/api/financial_data" + f"?page={page}&limit={limit}"
    response = client.get(url)
    assert response.status_code == 400


def test_incorrect_page_limit_type_4():
    page = 1
    limit = -0.5
    url = BASE_URL + "/api/financial_data" + f"?page={page}&limit={limit}"
    response = client.get(url)
    assert response.status_code == 422


def test_incorrect_symbol_1():
    symbol = "MSFT"
    endpoint = "/api/financial_data"
    url = BASE_URL + endpoint + f"?symbol={symbol}"
    response = client.get(url)
    assert response.status_code == 404


def test_incorrect_symbol_2():
    symbol = "SDFJLSADFSALFD"
    endpoint = "/api/financial_data"
    url = BASE_URL + endpoint + f"?symbol={symbol}"
    response = client.get(url)
    assert response.status_code == 400


def test_incorrect_symbol_3():
    symbol = "-11111111111"
    endpoint = "/api/financial_data"
    url = BASE_URL + endpoint + f"?symbol={symbol}"
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
