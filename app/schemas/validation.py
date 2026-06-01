import json
from pathlib import Path
import jsonschema

_SCHEMA_PATH = Path(__file__).parent / "contract_schema.json"
_SCHEMA = json.loads(_SCHEMA_PATH.read_text())


def validate_extraction(data: dict) -> list[str]:
    validator = jsonschema.Draft7Validator(_SCHEMA)
    errors = [e.message for e in validator.iter_errors(data)]
    return errors


def is_valid(data: dict) -> bool:
    return len(validate_extraction(data)) == 0
