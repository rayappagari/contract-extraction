import json
import os
from app.orchestration.pipeline import ExtractionPipeline
from app.storage.snowflake_writer import SnowflakeWriter

# -- Optional: wire up Snowflake -----------------------------------------
# Set these env vars to enable writing to Snowflake, otherwise runs extract-only.
sf_writer = None
if all(os.environ.get(v) for v in ["SNOWFLAKE_ACCOUNT", "SNOWFLAKE_USER", "SNOWFLAKE_PASSWORD"]):
    sf_writer = SnowflakeWriter(
        account=os.environ["SNOWFLAKE_ACCOUNT"],
        user=os.environ["SNOWFLAKE_USER"],
        password=os.environ["SNOWFLAKE_PASSWORD"],
        warehouse=os.environ.get("SNOWFLAKE_WAREHOUSE", "DEV_WH"),
        database=os.environ.get("SNOWFLAKE_DATABASE", "CONTRACTS_DEV"),
        schema=os.environ.get("SNOWFLAKE_SCHEMA", "EXTRACTED"),
    )
    sf_writer.create_table_if_not_exists()
    print("Snowflake connected. Results will be written.\n")
else:
    print("Snowflake env vars not set. Running extract-only.\n")
# ------------------------------------------------------------------------

pipeline = ExtractionPipeline(snowflake_writer=sf_writer)
result = pipeline.run("sample_contracts/acme_techvendor_msa.docx")

print("=" * 60)
print("EXTRACTED FIELDS")
print("=" * 60)
print(json.dumps(result["extracted"], indent=2))

print()
print("=" * 60)
print("QUALITY REPORT")
print("=" * 60)
print(f"Contract ID        : {result['contract_id']}")
print(f"Overall confidence : {result['scores']['overall']}")
print(f"Needs review       : {result['needs_review']}")
print(f"Validation errors  : {result['validation_errors'] or 'None'}")
print(f"Anomalies          : {result['anomalies'] or 'None'}")
print(f"Rule violations    : {result['rule_violations'] or 'None'}")

print()
print("FIELD SCORES")
for field, score in result["scores"]["field_scores"].items():
    bar = "#" * int(score * 10)
    print(f"  {field:<30} {bar:<10} {score}")

if sf_writer:
    sf_writer.close()
