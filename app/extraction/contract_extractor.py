import json
from app.extraction.claude_client import ClaudeClient
from app.extraction.prompt_builder import build_extraction_prompt, build_amendment_prompt
from app.extraction.retry_handler import with_retry


class ContractExtractor:
    def __init__(self, model: str = "claude-sonnet-4-6"):
        self.client = ClaudeClient(model=model)

    def extract(self, contract_text: str, prompt_version: str = "contract_extraction_v2.md") -> dict:
        system_prompt, user_message = build_extraction_prompt(contract_text, prompt_version)
        raw = with_retry(lambda: self.client.extract(system_prompt, user_message))
        return self._parse_response(raw)

    def extract_amendment(self, original_text: str, amendment_text: str) -> dict:
        system_prompt, user_message = build_amendment_prompt(original_text, amendment_text)
        raw = with_retry(lambda: self.client.extract(system_prompt, user_message))
        return self._parse_response(raw)

    def _parse_response(self, raw: str) -> dict:
        try:
            start = raw.find("{")
            end = raw.rfind("}") + 1
            return json.loads(raw[start:end])
        except (json.JSONDecodeError, ValueError) as e:
            raise ValueError(f"Failed to parse Claude response as JSON: {e}\nRaw: {raw[:500]}")
