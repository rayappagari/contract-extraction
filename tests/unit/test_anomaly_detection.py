import pytest
from app.quality.anomaly_detection import detect_anomalies


def test_expiration_before_effective_flagged():
    data = {"effective_date": "2025-01-01", "expiration_date": "2024-01-01", "parties": [{"name": "X"}]}
    anomalies = detect_anomalies(data)
    assert any("expiration_date" in a for a in anomalies)


def test_negative_value_flagged():
    data = {"total_value": -5000, "parties": [{"name": "X"}]}
    anomalies = detect_anomalies(data)
    assert any("negative" in a for a in anomalies)


def test_clean_contract_no_anomalies():
    data = {
        "effective_date": "2024-01-01",
        "expiration_date": "2025-01-01",
        "total_value": 50000,
        "parties": [{"name": "Acme", "role": "buyer"}],
    }
    assert detect_anomalies(data) == []
