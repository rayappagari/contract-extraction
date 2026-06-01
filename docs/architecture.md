# Architecture

## System Overview

```mermaid
graph TB
    subgraph Clients
        CLI[CLI / Script]
        API[Internal API]
    end

    subgraph Orchestration Layer
        BR[batch_runner.py\nThreadPoolExecutor]
        PL[pipeline.py\nExtractionPipeline]
    end

    subgraph Ingestion Layer
        FR[file_router.py]
        PDF[pdf_loader.py\npdfplumber]
        DOCX[docx_loader.py\npython-docx]
        OCR[ocr_processor.py\nTesseract]
    end

    subgraph Preprocessing Layer
        TC[text_cleaner.py]
        CH[chunking.py]
    end

    subgraph Extraction Layer
        PB[prompt_builder.py]
        CC[claude_client.py\nAnthropic SDK]
        CE[contract_extractor.py]
        RH[retry_handler.py]
    end

    subgraph Quality Layer
        VS[validation.py\nJSON Schema]
        CS[confidence_scoring.py]
        AD[anomaly_detection.py]
        BR2[business_rules.py]
    end

    subgraph Storage Layer
        SW[snowflake_writer.py]
        S3[s3_writer.py]
        RQ[review_queue.py\nSQS]
    end

    CLI --> BR
    API --> BR
    BR --> PL
    PL --> FR
    FR --> PDF
    FR --> DOCX
    PDF -->|scanned| OCR
    PDF --> TC
    DOCX --> TC
    OCR --> TC
    TC --> CH
    CH --> PB
    PB --> CE
    CE --> CC
    CC -->|fail| RH
    RH --> CC
    CC --> CE
    CE --> VS
    VS --> CS
    CS --> AD
    AD --> BR2
    BR2 -->|pass| SW
    BR2 -->|pass| S3
    BR2 -->|fail| RQ

    style CC fill:#4A90D9,color:#fff
    style SW fill:#29B5E8,color:#fff
    style S3 fill:#FF9900,color:#fff
    style RQ fill:#E8433A,color:#fff
    style OCR fill:#7B68EE,color:#fff
```

---

## Module Responsibilities

### Orchestration

| Module | Responsibility |
|--------|---------------|
| `pipeline.py` | Wires all stages for a single file; returns a result dict with extracted data, scores, anomalies, and review flag |
| `batch_runner.py` | Parallelizes pipeline across a list of files using `ThreadPoolExecutor`; aggregates results and errors |

### Ingestion

| Module | Library | Notes |
|--------|---------|-------|
| `pdf_loader.py` | pdfplumber | Extracts text per page; preserves page metadata for chunking |
| `docx_loader.py` | python-docx | Joins non-empty paragraphs; treats whole document as single page |
| `ocr_processor.py` | pytesseract | Applied only when a PDF page returns empty text |
| `file_router.py` | — | Dispatches on file extension; raises `ValueError` for unsupported types |

### Preprocessing

```mermaid
flowchart LR
    RAW[Raw Page Text] --> A[strip non-ASCII\nnon-printable chars]
    A --> B[collapse whitespace\nremove hyphenation]
    B --> C[normalize blank lines]
    C --> D[page-aware chunking\nmax_chars with overlap]
    D --> CHUNKS[Text Chunks]
```

**Chunking strategy:** Pages are grouped until the combined character count exceeds `max_chars` (default 8,000). Each chunk tracks which page numbers it spans — useful for citation back to the source document.

### Extraction

```mermaid
sequenceDiagram
    participant E as contract_extractor
    participant P as prompt_builder
    participant C as claude_client
    participant R as retry_handler

    E->>P: build_extraction_prompt(text, version)
    P-->>E: (system_prompt, user_message)
    E->>R: with_retry(lambda: client.extract(...))
    loop Up to max_attempts
        R->>C: messages.create(model, temp=0, ...)
        alt Success
            C-->>R: raw JSON string
        else API error / timeout
            R->>R: sleep(2^attempt)
        end
    end
    R-->>E: raw JSON string
    E->>E: parse JSON from raw
    E-->>Caller: extracted dict
```

**Design decisions:**
- `temperature=0.0` — deterministic output for consistent field extraction
- JSON parsed by finding the first `{` and last `}` — tolerant of preamble text
- Amendment extraction uses a separate prompt that diffs original vs. amendment text

### Quality Gates

```mermaid
flowchart TD
    A[Extracted Dict] --> B

    B[JSON Schema Validation\nDraft-07]
    B -->|errors| LOG1[log validation_errors]
    B --> C

    C[Confidence Scoring\nscore = 0.8×required + 0.2×optional]
    C --> D{score ≥ threshold\ndev=0.75 prod=0.85}
    D -->|below| REVIEW[needs_review = True]
    D -->|above| E

    E[Anomaly Detection]
    E --> F{anomalies?}
    F -->|yes| REVIEW
    F -->|no| G

    G[Business Rules]
    G --> H{violations?}
    H -->|yes| REVIEW
    H -->|no| OK[needs_review = False]
```

**Confidence weight rationale:** Required fields (parties, dates, value, terms, jurisdiction) are the fields downstream systems rely on. Optional fields improve completeness but a missing SLA list shouldn't block automated processing.

**Anomaly checks:**
- `expiration_date` must be after `effective_date`
- `total_value` must be non-negative
- `liability_cap` must be < 10× `total_value`
- At least one party must be identified

**Business rule checks:**
- `contract_type` must be a known enum value
- At least one buyer or licensee party required
- If `auto_renewal = true`, `renewal_notice_days` must be present

### Storage

```mermaid
graph LR
    R[Result Dict]

    R -->|structured fields| SF[(Snowflake\nCONTRACTS table)]
    R -->|full JSON artifact| S3[(S3\ncontracts/YYYY/MM/DD/id.json)]
    R -->|raw text| S3R[(S3\ncontracts/raw/id.txt)]
    R -->|if needs_review| SQS[SQS Queue\nhuman review workflow]

    style SF fill:#29B5E8,color:#fff
    style S3 fill:#FF9900,color:#fff
    style S3R fill:#FF9900,color:#fff
    style SQS fill:#E8433A,color:#fff
```

---

## Deployment Environments

| Concern | Dev | QA | Prod |
|---------|-----|----|------|
| Workers | 2 | 4 | 8 |
| Confidence threshold | 0.75 | 0.80 | 0.85 |
| Claude retries | 3 | 3 | 5 |
| Snowflake DB | CONTRACTS_DEV | CONTRACTS_QA | CONTRACTS_PROD |
| Log level | DEBUG | INFO | WARNING |

---

## Error Handling Strategy

```mermaid
flowchart TD
    E[Error occurs]
    E --> A{Layer?}
    A -->|Ingestion| B[raise ValueError\nunsupported type]
    A -->|Claude API| C[retry_handler\nexponential backoff\nmax 3-5 attempts]
    C -->|exhausted| D[raise RuntimeError\nlog full trace]
    A -->|JSON parse| F[raise ValueError\nlog raw response excerpt]
    A -->|Batch| G[catch per-file\nlog error\ncontinue batch\nreturn error entry]
```

No single file failure aborts the batch — errors are captured per-file and the batch continues.
