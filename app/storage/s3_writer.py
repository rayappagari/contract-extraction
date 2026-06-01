import json
import boto3
from datetime import datetime


class S3Writer:
    def __init__(self, bucket: str, prefix: str = "contracts/", region: str = "us-east-1"):
        self.bucket = bucket
        self.prefix = prefix
        self.s3 = boto3.client("s3", region_name=region)

    def write_contract(self, contract_id: str, data: dict) -> str:
        key = f"{self.prefix}{datetime.utcnow().strftime('%Y/%m/%d')}/{contract_id}.json"
        self.s3.put_object(
            Bucket=self.bucket,
            Key=key,
            Body=json.dumps(data, indent=2),
            ContentType="application/json",
        )
        return key

    def write_raw(self, contract_id: str, raw_text: str) -> str:
        key = f"{self.prefix}raw/{contract_id}.txt"
        self.s3.put_object(Bucket=self.bucket, Key=key, Body=raw_text, ContentType="text/plain")
        return key
