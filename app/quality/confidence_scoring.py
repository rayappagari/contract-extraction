REQUIRED_FIELDS = ["parties", "effective_date", "expiration_date", "total_value", "governing_law", "payment_terms"]
OPTIONAL_FIELDS = ["auto_renewal", "renewal_notice_days", "liability_cap", "sla_terms", "key_obligations"]


def score_extraction(data: dict) -> dict[str, float]:
    scores = {}
    for field in REQUIRED_FIELDS:
        value = data.get(field)
        scores[field] = 1.0 if value not in (None, "", []) else 0.0
    for field in OPTIONAL_FIELDS:
        value = data.get(field)
        scores[field] = 1.0 if value not in (None, "", []) else 0.0
    required_avg = sum(scores[f] for f in REQUIRED_FIELDS) / len(REQUIRED_FIELDS)
    optional_avg = sum(scores[f] for f in OPTIONAL_FIELDS) / len(OPTIONAL_FIELDS)
    overall = 0.8 * required_avg + 0.2 * optional_avg
    return {"field_scores": scores, "overall": round(overall, 4)}


def is_high_confidence(scores: dict, threshold: float = 0.75) -> bool:
    return scores.get("overall", 0.0) >= threshold
