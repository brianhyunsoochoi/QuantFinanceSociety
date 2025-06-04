import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../backend')))

from main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_simulate_monthly_success():
    payload = {
        "tickers": ["AAPL"],
        "amounts": [10000],
        "strategy": "monthly"
    }
    response = client.post("/simulate", json=payload)
    assert response.status_code == 200
    data = response.json()

    assert "results" in data
    assert len(data["results"]) == 1
    result = data["results"][0]

    assert result["ticker"] == "AAPL"
    assert isinstance(result["final_value"], (float, int, type(None)))
    assert isinstance(result["prices"], list)

def test_simulate_lump_sum_success():
    payload = {
        "tickers": ["MSFT"],
        "amounts": [5000],
        "strategy": "lump_sum"
    }
    response = client.post("/simulate", json=payload)
    assert response.status_code == 200
    data = response.json()
    result = data["results"][0]

    assert result["ticker"] == "MSFT"
    assert isinstance(result["final_value"], (float, int, type(None)))
    assert isinstance(result["prices"], list)

def test_simulate_invalid_strategy():
    payload = {
        "tickers": ["TSLA"],
        "amounts": [3000],
        "strategy": "invalid_strategy"
    }
    response = client.post("/simulate", json=payload)
    assert response.status_code == 200
    result = response.json()["results"][0]
    assert result["final_value"] is None
    assert result["prices"] == []

def test_simulate_mismatched_lists():
    payload = {
        "tickers": ["AAPL", "GOOG"],
        "amounts": [10000],
        "strategy": "monthly"
    }
    response = client.post("/simulate", json=payload)
    assert response.status_code == 200
    assert len(response.json()["results"]) == 1  # zip 때문에 하나만 처리됨