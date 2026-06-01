import json
import snowflake.connector
from typing import Any


class SnowflakeWriter:
    def __init__(self, account: str, user: str, password: str, warehouse: str, database: str, schema: str):
        self.conn = snowflake.connector.connect(
            account=account, user=user, password=password,
            warehouse=warehouse, database=database, schema=schema,
        )

    def write_contract(self, contract_id: str, data: dict, scores: dict) -> None:
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO contracts (contract_id, data, confidence_scores, created_at) "
            "VALUES (%s, PARSE_JSON(%s), PARSE_JSON(%s), CURRENT_TIMESTAMP())",
            (contract_id, json.dumps(data), json.dumps(scores)),
        )
        self.conn.commit()
        cursor.close()

    def close(self) -> None:
        self.conn.close()
