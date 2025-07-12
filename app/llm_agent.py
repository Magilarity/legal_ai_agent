import time
from typing import List

import openai


class LLMAgent:
    """
    LLM agent with retry, backoff, streaming and batching support.
    """

    def __init__(
        self,
        api_key: str,
        model: str,
        max_retries: int = 3,
        backoff_factor: float = 0.5,
        stream: bool = False,
    ):
        openai.api_key = api_key
        self.model = model
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor
        self.stream = stream

    def chat(self, prompt: str) -> str:
        """
        Send a single prompt to the model. Supports streaming if enabled.
        """
        attempts = 0
        while True:
            try:
                response = openai.ChatCompletion.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    stream=self.stream,
                )
                if self.stream:
                    result = ""
                    for chunk in response:
                        delta = chunk.choices[0].delta.get("content")
                        if delta:
                            result += delta
                    return result
                if not isinstance(response, dict) or "choices" not in response:
                    raise ValueError("Invalid response format: missing 'choices'")
                choices = response["choices"]
                if not choices:
                    raise ValueError("Invalid response format: empty 'choices'")
                return choices[0]["message"]["content"]
            except Exception:
                if attempts >= self.max_retries:
                    raise
                backoff = self.backoff_factor * (2**attempts)
                time.sleep(backoff)
                attempts += 1

    def chat_batch(self, prompts: List[str], batch_size: int = 5) -> List[str]:
        """
        Send multiple prompts in batches. Returns list of responses.
        """
        results: List[str] = []
        for i in range(0, len(prompts), batch_size):
            batch = prompts[i : i + batch_size]
            for prompt in batch:
                results.append(self.chat(prompt))
        return results
