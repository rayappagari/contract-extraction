import json
import os
from app.orchestration.pipeline import ExtractionPipeline
from app.storage.snowflake_writer import SnowflakeWriter

sf = SnowflakeWriter(
    account=os.environ["SNOWFLAKE_ACCOUNT"],
    user=os.environ["SNOWFLAKE_USER"],
    password=os.environ["SNOWFLAKE_PASSWORD"],
    warehouse=os.environ.get("SNOWFLAKE_WAREHOUSE", "COMPUTE_WH"),
    database=os.environ.get("SNOWFLAKE_DATABASE", "CONTRACTS_DEV"),
    schema=os.environ.get("SNOWFLAKE_SCHEMA", "EXTRACTED"),
)

print("Connected to Snowflake. Creating tables if not exist...")
sf.create_tables_if_not_exist()
print("Tables ready.\n")

pipeline = ExtractionPipeline(snowflake_writer=sf)

contracts = [
    "sample_contracts/acme_techvendor_msa.docx",
    "sample_contracts/globaltech_databridge_sow.pdf",
]

for path in contracts:
    print(f"Processing: {path}")
    result = pipeline.run(path)
    print(f"  Contract ID  : {result['contract_id']}")
    print(f"  Type         : {result['extracted'].get('contract_type')}")
    print(f"  Vendor       : {next((p['name'] for p in result['extracted'].get('parties', []) if p.get('role') in ('vendor','seller')), 'N/A')}")
    print(f"  Confidence   : {result['scores']['overall']}")
    print(f"  Needs review : {result['needs_review']}")
    print(f"  Snowflake    : written\n")

sf.close()
print("Done. Both contracts written to Snowflake.")
