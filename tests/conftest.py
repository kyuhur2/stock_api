import os
import socket
import pytest
from fastapi.testclient import TestClient
from financial.app import app
from functools import wraps


# constants
HOST = "127.0.0.1"
PORT = 5000
BASE_URL = f"http://{HOST}:{PORT}"
DATABASE_NAME = "financial_data.db"
client = TestClient(app)


def check_server_running():
    def server_running():
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            return sock.connect_ex((HOST, PORT)) == 0

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not server_running():
                pytest.skip("Server is not running")
            return func(*args, **kwargs)

        return wrapper

    return decorator


def check_db_exists():
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            project_root = os.path.join(os.path.dirname(__file__), "..")
            if os.path.exists(os.path.join(project_root, DATABASE_NAME)):
                return func(*args, **kwargs)
            else:
                pytest.skip("Database not found")

        return wrapper

    return decorator


def pytest_collection_modifyitems(config, items):
    for item in items:
        item.obj = check_db_exists()(item.obj)
        item.obj = check_server_running()(item.obj)
