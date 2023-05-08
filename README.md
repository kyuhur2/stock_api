# Stock API

Project purpose outlined [here](/docs/README.md).

## Project Description

### Section 1 - Create a financial data storage server

1. Storing API keys safely **(THIS STEP IS NECESSARY FOR STEP 2)**

    1.1. Locally (assumes `python-dotenv` is downloaded)
    - Create an `.env` file in the parent-most directory
    - Add the API key in the file with `ALPHA_VANTAGE_API_KEY=<insert_api_key_here>`

    1.2. Production
    - Set the API key as an environment variable directly with `export ALPHA_VANTAGE_API_KEY=<insert_api_key_here>`
    **OR**
    - Add the `ALPHA_VANTAGE_API_KEY` variable on the deployment platform environment through the management system

2. Running the project **(THIS STEP IS NECESSARY FOR NEXT SECTION)**

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

### Section 2 - Create an API service to make GET calls on database

1. Pretest setup (assumes that `python get_raw_data.py` was already executed and a `financial_data.db` exists in the parent-most directory)

        cd ~/stock_api
        source stock_api_env/bin/activate   # assumes virtual environment exists
        pip install -e .  # important step to make financial/ a module

2. Running the server

        docker-compose up --build

    Default port is `5000`. To change, alter settings on `Dockerfile`, `docker-compose.yaml`, and `tests/conftest.py`.

3. Running pytests

- Verify that server is running on port `5000`
- Verify that `financial_data.db` exists in the parent-most folder by running `python get_raw_data.py`
- If either are not running properly, the below pytests will be skipped

        cd ~/stock_api
        pytest tests/unit  # there are no integration tests currently


4. Things to note
- Requires `Python 3.8`
- Built with [FastAPI](https://fastapi.tiangolo.com/), version 0.95.1

### Miscellaneous

- Added CI
- Added branch rules on main (have to submit PRs to merge changes, have to pass CI to merge, etc.)
- Added tests under the `tests` folder (only unit tests for now but integration tests can be added later)
