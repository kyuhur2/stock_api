# Stock API Project

## Project Description

**Project purpose is outlined in the [next section](#Purpose).**

### Section 1 - Create a financial data storage server

1. Storing API keys safely **(THIS STEP IS NECESSARY FOR STEP 2)**

    1.1. Locally (assumes `python-dotenv` is downloaded)
    - Create an `.env` file in the parent-most directory
    - Add the API key in the file with `ALPHA_VANTAGE_API_KEY=<insert_api_key_here>`

    1.2. Production
    - Set the API key as an environment variable directly with `export ALPHA_VANTAGE_API_KEY=<insert_api_key_here>`
    **OR**
    - Add the `ALPHA_VANTAGE_API_KEY` variable on the deployment platform environment through the management system

2. Running the project

        cd ~/stock_api
        pip install -r requirements.txt
        virtualenv stock_api_env  # python -m venv stock_api_env if no global virtualenv
        source stock_api_env/bin/activate  # env\Scripts\activate.bat for Windows
        python get_raw_data.py

3. Things to note
- Database is initialized if no database exists (`SQLite3` by default)
- Duplicate entries in the database is not allowed
- Logs are recorded in `./logs/logs.log`, `./logs` directory is created if it doesn't exist
- Errors from API, data, etc. are handled in `AlphaVantageProvider.get_stock_data()`
- All components adhere to SOLID principles -- while this project is simple and can be done in one file, maintainability and extensibility is important

## Purpose

### Create a financial data storage server

1. Obtain financial data for two specific stocks (IBM and Apple Inc.) for the past two weeks up with [AlphaVantage](https://www.alphavantage.co/documentation/)

2. Process the raw data response from the API. The expected result following processing should resemble the following sample output:

```
{
    "symbol": "IBM",
    "date": "2023-02-14",
    "open_price": "153.08",
    "close_price": "154.52",
    "volume": "62199013",
},
{
    "symbol": "IBM",
    "date": "2023-02-13",
    "open_price": "153.08",
    "close_price": "154.52",
    "volume": "59099013"
},
{
    "symbol": "IBM",
    "date": "2023-02-12",
    "open_price": "153.08",
    "close_price": "154.52",
    "volume": "42399013"
},
...
```
3. Add entries to a database table titled `financial_data` on a local server. Use the exact same column names as those derived from the data processing conducted in step 2 (`symbol`, `date`, `open_price`, `close_price`, `volume`).

### Create an API to retrieve financial data from storage server

1. Develop an API that utilizes the `GET` method to fetch financial data records from the `financial_data` table. Restrictions:
- Endpoint must be able to receive optional parameters such as `start_date`, `end_date`, and `symbol`.
- Endpoint must support pagination using the `limit` and `page` parameters. If these parameters are not provided, the default limit for a single page should be set to 5.
- Endpoint should generate a result that contains the following three properties:
    - `data`: an array includes the data
    - `pagination`: handling of pagination for four properties
        - `count`: count of all records without pagination
        - `page`: current page index
        - `limit`: limit of records that can be retrieved for a single page (default: 5)
        - `pages`: total number of pages
    - `info`: includes any error info (if applicable)


Sample Request:
```bash
curl -X GET 'http://localhost:5000/api/financial_data?start_date=2023-01-01&end_date=2023-01-14&symbol=IBM&limit=3&page=2'
```

Sample Response:
```
{
    "data": [
        {
            "symbol": "IBM",
            "date": "2023-01-05",
            "open_price": "153.08",
            "close_price": "154.52",
            "volume": "62199013",
        },
        {
            "symbol": "IBM",
            "date": "2023-01-06",
            "open_price": "153.08",
            "close_price": "154.52",
            "volume": "59099013"
        },
        {
            "symbol": "IBM",
            "date": "2023-01-09",
            "open_price": "153.08",
            "close_price": "154.52",
            "volume": "42399013"
        }
    ],
    "pagination": {
        "count": 20,
        "page": 2,
        "limit": 3,
        "pages": 7
    },
    "info": {'error': ''}
}

```

2. Implement a `GET` statistics API to perform calculations on data in a given period of time:
- Average daily open price for the period
- Average daily closing price for the period
- Average daily volume for the period

- Endpoint should accept the following parameters as REQUIRED parameters:
    - `start_date`
    - `end_date`
    - `symbols`
- Endpoint should return a result with two properties:
    - `data`: calculated statistics
    - `info`: includes any error info (if applicable)

Sample Request:
```bash
curl -X GET http://localhost:5000/api/statistics?start_date=2023-01-01&end_date=2023-01-31&symbol=IBM
```

Sample Response:
```
{
    "data": {
        "start_date": "2023-01-01",
        "end_date": "2023-01-31",
        "symbol": "IBM",
        "average_daily_open_price": 123.45,
        "average_daily_close_price": 234.56,
        "average_daily_volume": 1000000
    },
    "info": {'error': ''}
}

```
