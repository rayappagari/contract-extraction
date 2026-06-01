from datetime import date, datetime
from typing import Optional


def detect_anomalies(data: dict) -> list[str]:
    anomalies = []
    effective = _parse_date(data.get("effective_date"))
    expiration = _parse_date(data.get("expiration_date"))
    if effective and expiration and expiration <= effective:
        anomalies.append("expiration_date is not after effective_date")
    total_value = data.get("total_value")
    if total_value is not None and total_value < 0:
        anomalies.append("total_value is negative")
    liability_cap = data.get("liability_cap")
    if liability_cap is not None and total_value is not None and liability_cap > total_value * 10:
        anomalies.append("liability_cap is unusually high relative to total_value")
    if not data.get("parties"):
        anomalies.append("no parties identified")
    return anomalies


def _parse_date(value: Optional[str]) -> Optional[date]:
    if not value:
        return None
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        return None
