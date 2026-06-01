import json
import boto3


class ReviewQueue:
    def __init__(self, queue_url: str, region: str = "us-east-1"):
        self.queue_url = queue_url
        self.sqs = boto3.client("sqs", region_name=region)

    def enqueue(self, contract_id: str, reason: str, data: dict) -> str:
        body = json.dumps({"contract_id": contract_id, "reason": reason, "data": data})
        response = self.sqs.send_message(QueueUrl=self.queue_url, MessageBody=body)
        return response["MessageId"]

    def receive(self, max_messages: int = 10) -> list[dict]:
        response = self.sqs.receive_message(
            QueueUrl=self.queue_url,
            MaxNumberOfMessages=max_messages,
            WaitTimeSeconds=5,
        )
        return response.get("Messages", [])
