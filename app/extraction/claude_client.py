import anthropic
from typing import Optional


class ClaudeClient:
    def __init__(self, model: str = "claude-sonnet-4-6", max_tokens: int = 4096):
        self.client = anthropic.Anthropic()
        self.model = model
        self.max_tokens = max_tokens

    def extract(self, system_prompt: str, user_message: str, temperature: float = 0.0) -> str:
        response = self.client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            temperature=temperature,
            system=system_prompt,
            messages=[{"role": "user", "content": user_message}],
        )
        return response.content[0].text
