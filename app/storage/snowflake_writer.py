import json
import snowflake.connector


# Term types written to CONTRACT_TERMS as individual rows
SCALAR_TERMS = [
    "total_value", "currency", "payment_terms", "governing_law",
    "auto_renewal", "renewal_notice_days", "termination_for_convenience", "liability_cap",
]


class SnowflakeWriter:
    def __init__(self, account: str, user: str, password: str, warehouse: str, database: str, schema: str):
        self.conn = snowflake.connector.connect(
            account=account, user=user, password=password,
            warehouse=warehouse, database=database, schema=schema,
        )

    def create_tables_if_not_exist(self) -> None:
        import pathlib
        ddl = (pathlib.Path(__file__).parents[2] / "sql" / "create_tables.sql").read_text()
        cursor = self.conn.cursor()
        for statement in ddl.split(";"):
            stmt = statement.strip()
            if stmt:
                cursor.execute(stmt)
        self.conn.commit()
        cursor.close()

    def write_contract(self, contract_id: str, source_file: str, data: dict, scores: dict,
                       model_version: str, needs_review: bool,
                       validation_errors: list, anomalies: list, rule_violations: list) -> None:
        self._write_header(contract_id, source_file, data)
        self._write_terms(contract_id, data)
        self._write_audit(contract_id, model_version, scores, needs_review,
                          validation_errors, anomalies, rule_violations)
        self.conn.commit()

    def _write_header(self, contract_id: str, source_file: str, data: dict) -> None:
        vendor = next(
            (p["name"] for p in data.get("parties", []) if p.get("role") in ("vendor", "seller")),
            None,
        )
        buyer = next(
            (p["name"] for p in data.get("parties", []) if p.get("role") in ("buyer", "licensee")),
            None,
        )
        self.conn.cursor().execute(
            """
            INSERT INTO CONTRACT_HEADER
                (contract_id, contract_type, vendor, buyer, start_date, end_date, source_file)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (
                contract_id,
                data.get("contract_type"),
                vendor,
                buyer,
                data.get("effective_date"),
                data.get("expiration_date"),
                source_file,
            ),
        )

    def _write_terms(self, contract_id: str, data: dict) -> None:
        rows = []
        for term in SCALAR_TERMS:
            value = data.get(term)
            if value is not None:
                rows.append((contract_id, term, str(value)))
        for sla in data.get("sla_terms", []):
            rows.append((contract_id, "sla_term", sla))
        for obligation in data.get("key_obligations", []):
            rows.append((contract_id, "key_obligation", obligation))
        if rows:
            self.conn.cursor().executemany(
                "INSERT INTO CONTRACT_TERMS (contract_id, term_type, value) VALUES (%s, %s, %s)",
                rows,
            )

    def _write_audit(self, contract_id: str, model_version: str, scores: dict,
                     needs_review: bool, validation_errors: list,
                     anomalies: list, rule_violations: list) -> None:
        self.conn.cursor().execute(
            """
            INSERT INTO CONTRACT_EXTRACTION_AUDIT
                (contract_id, model_version, confidence, needs_review,
                 validation_errors, anomalies, rule_violations)
            VALUES (%s, %s, %s, %s, PARSE_JSON(%s), PARSE_JSON(%s), PARSE_JSON(%s))
            """,
            (
                contract_id,
                model_version,
                scores.get("overall"),
                needs_review,
                json.dumps(validation_errors),
                json.dumps(anomalies),
                json.dumps(rule_violations),
            ),
        )

    def close(self) -> None:
        self.conn.close()
