# Stock API Project

## Goals

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
