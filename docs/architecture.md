# Architecture

## Overview

The contract extraction pipeline ingests PDF and DOCX files, cleans and chunks the text, extracts structured fields using Claude, validates the output, and writes results to Snowflake and S3. Low-confidence results are routed to a human review queue via SQS.

## Component Map

```
File Input (PDF/DOCX)
    └── ingestion/file_router.py
        ├── ingestion/pdf_loader.py
        └── ingestion/docx_loader.py
            └── preprocessing/ocr_processor.py (scanned PDFs)

Text Preprocessing
    └── preprocessing/text_cleaner.py
    └── preprocessing/chunking.py

Extraction
    └── extraction/contract_extractor.py
        ├── extraction/prompt_builder.py
        ├── extraction/claude_client.py
        └── extraction/retry_handler.py

Quality
    ├── schemas/validation.py          — JSON schema enforcement
    ├── quality/confidence_scoring.py  — field-level confidence
    ├── quality/anomaly_detection.py   — date/value sanity checks
    └── quality/business_rules.py      — domain rule enforcement

Storage
    ├── storage/snowflake_writer.py    — structured fields
    ├── storage/s3_writer.py           — raw + JSON artifacts
    └── storage/review_queue.py        — SQS for human review

Orchestration
    ├── orchestration/pipeline.py      — single-file pipeline
    └── orchestration/batch_runner.py  — parallel batch processing
```

## Data Flow

1. File is routed by extension to the appropriate loader.
2. Text is cleaned, normalized, and chunked to fit within context limits.
3. Claude extracts a JSON payload from the full contract text.
4. The response is validated against the JSON schema.
5. Confidence scores and anomaly checks gate automated vs. manual review.
6. Results are written to Snowflake (structured) and S3 (raw + JSON).
7. Low-confidence results are enqueued in SQS for human review.
