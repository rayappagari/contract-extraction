from datetime import datetime


DATE_FIELDS = {"effective_date", "expiration_date"}
NUMERIC_FIELDS = {"total_value", "liability_cap", "renewal_notice_days"}


def score_field(predicted, actual, field: str) -> float:
    if actual is None:
        return 1.0 if predicted is None else 0.0
    if predicted is None:
        return 0.0
    if field in DATE_FIELDS:
        return _date_match(predicted, actual)
    if field in NUMERIC_FIELDS:
        return _numeric_match(predicted, actual)
    return 1.0 if str(predicted).strip().lower() == str(actual).strip().lower() else 0.0


def score_result(extracted: dict, ground_truth: dict, fields: list[str]) -> dict[str, float]:
    field_scores = {f: score_field(extracted.get(f), ground_truth.get(f), f) for f in fields}
    overall = sum(field_scores.values()) / len(field_scores) if field_scores else 0.0
    return {"field_scores": field_scores, "overall": round(overall, 4)}


def _date_match(pred: str, actual: str) -> float:
    try:
        return 1.0 if datetime.strptime(pred, "%Y-%m-%d") == datetime.strptime(actual, "%Y-%m-%d") else 0.0
    except ValueError:
        return 0.0


def _numeric_match(pred, actual, tolerance: float = 0.01) -> float:
    try:
        return 1.0 if abs(float(pred) - float(actual)) / (abs(float(actual)) + 1e-9) <= tolerance else 0.0
    except (TypeError, ValueError):
        return 0.0
