import logging
from pathlib import Path
from app.ingestion.file_router import route_file
from app.preprocessing.text_cleaner import clean_text, normalize_whitespace
from app.preprocessing.chunking import chunk_by_pages
from app.extraction.contract_extractor import ContractExtractor
from app.schemas.validation import validate_extraction
from app.quality.confidence_scoring import score_extraction, is_high_confidence
from app.quality.anomaly_detection import detect_anomalies
from app.quality.business_rules import apply_business_rules

logger = logging.getLogger(__name__)


class ExtractionPipeline:
    def __init__(self, model: str = "claude-sonnet-4-6"):
        self.extractor = ContractExtractor(model=model)

    def run(self, file_path: str) -> dict:
        logger.info(f"Processing: {file_path}")
        raw = route_file(file_path)
        pages = raw.get("pages") or [{"page": 1, "text": raw.get("text", "")}]
        for page in pages:
            page["text"] = normalize_whitespace(clean_text(page["text"]))
        chunks = chunk_by_pages(pages)
        contract_text = "\n\n".join(c["text"] for c in chunks)
        extracted = self.extractor.extract(contract_text)
        validation_errors = validate_extraction(extracted)
        scores = score_extraction(extracted)
        anomalies = detect_anomalies(extracted)
        rule_violations = apply_business_rules(extracted)
        needs_review = not is_high_confidence(scores) or bool(anomalies) or bool(rule_violations)
        return {
            "file": str(file_path),
            "extracted": extracted,
            "scores": scores,
            "validation_errors": validation_errors,
            "anomalies": anomalies,
            "rule_violations": rule_violations,
            "needs_review": needs_review,
        }
