import pytest
from app.quality.confidence_scoring import score_extraction, is_high_confidence


def test_full_extraction_scores_high():
    data = {
        "parties": [{"name": "Acme", "role": "buyer"}],
        "effective_date": "2024-01-01",
        "expiration_date": "2025-01-01",
        "total_value": 100000,
        "governing_law": "New York",
        "payment_terms": "Net 30",
    }
    scores = score_extraction(data)
    assert scores["overall"] > 0.75
    assert is_high_confidence(scores)


def test_empty_extraction_scores_low():
    scores = score_extraction({})
    assert scores["overall"] == 0.0
    assert not is_high_confidence(scores)
