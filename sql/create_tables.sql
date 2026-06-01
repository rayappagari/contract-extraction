-- CONTRACT_HEADER: one row per contract
CREATE TABLE IF NOT EXISTS CONTRACT_HEADER (
    contract_id     VARCHAR        NOT NULL,
    contract_type   VARCHAR,
    vendor          VARCHAR,
    buyer           VARCHAR,
    start_date      DATE,
    end_date        DATE,
    source_file     VARCHAR,
    created_at      TIMESTAMP_NTZ  DEFAULT CURRENT_TIMESTAMP(),
    PRIMARY KEY (contract_id)
);

-- CONTRACT_TERMS: one row per term per contract (key-value)
CREATE TABLE IF NOT EXISTS CONTRACT_TERMS (
    id              INTEGER        AUTOINCREMENT PRIMARY KEY,
    contract_id     VARCHAR        NOT NULL,
    term_type       VARCHAR        NOT NULL,
    value           VARCHAR,
    FOREIGN KEY (contract_id) REFERENCES CONTRACT_HEADER(contract_id)
);

-- CONTRACT_EXTRACTION_AUDIT: one row per extraction run
CREATE TABLE IF NOT EXISTS CONTRACT_EXTRACTION_AUDIT (
    audit_id        INTEGER        AUTOINCREMENT PRIMARY KEY,
    contract_id     VARCHAR        NOT NULL,
    model_version   VARCHAR,
    confidence      FLOAT,
    needs_review    BOOLEAN,
    validation_errors VARIANT,
    anomalies         VARIANT,
    rule_violations   VARIANT,
    extracted_at    TIMESTAMP_NTZ  DEFAULT CURRENT_TIMESTAMP(),
    FOREIGN KEY (contract_id) REFERENCES CONTRACT_HEADER(contract_id)
);

-- Views
CREATE OR REPLACE VIEW contracts_expiring_soon AS
SELECT
    h.contract_id,
    h.contract_type,
    h.vendor,
    h.buyer,
    h.start_date,
    h.end_date,
    DATEDIFF('day', CURRENT_DATE(), h.end_date) AS days_until_expiry,
    a.confidence
FROM CONTRACT_HEADER h
JOIN CONTRACT_EXTRACTION_AUDIT a USING (contract_id)
WHERE h.end_date BETWEEN CURRENT_DATE() AND DATEADD('day', 90, CURRENT_DATE())
ORDER BY h.end_date ASC;

CREATE OR REPLACE VIEW contracts_for_review AS
SELECT
    h.contract_id,
    h.vendor,
    h.contract_type,
    h.source_file,
    a.confidence,
    a.needs_review,
    a.validation_errors,
    a.anomalies,
    a.extracted_at
FROM CONTRACT_HEADER h
JOIN CONTRACT_EXTRACTION_AUDIT a USING (contract_id)
WHERE a.needs_review = TRUE
ORDER BY a.extracted_at DESC;
