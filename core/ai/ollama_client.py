"""Minimal Ollama HTTP client for Javis.

Uses only the Python standard library so the project does not need an extra
package. It talks to Ollama's /api/generate endpoint and returns plain text.
"""

from __future__ import annotations

import json
import re
import urllib.error
import urllib.request
from typing import Optional

from core.ai.ollama_config import OLLAMA_BASE_URL, OLLAMA_MODEL_NAME, OLLAMA_TIMEOUT, OLLAMA_ENABLED


class OllamaClient:
    def __init__(self, base_url: str = OLLAMA_BASE_URL, model: str = OLLAMA_MODEL_NAME, timeout: int = OLLAMA_TIMEOUT):
        if not base_url:
            raise ValueError("Ollama base URL is empty; set OLLAMA_BASE_URL or core.ai.ollama_config.OLLAMA_BASE_URL")
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.timeout = timeout
        self.enabled = OLLAMA_ENABLED

    def _clean_response(self, text: str) -> str:
        text = re.sub(r"<think>.*?</think>", "", text or "", flags=re.DOTALL | re.IGNORECASE)
        text = re.sub(r"<think>.*$", "", text, flags=re.DOTALL | re.IGNORECASE)
        text = re.sub(r"</?think>", "", text, flags=re.IGNORECASE)
        return text.strip()

    def is_available(self) -> bool:
        if not self.enabled:
            return False
        try:
            req = urllib.request.Request(self.base_url + "/api/tags", headers={"User-Agent": "Javis/1.0"})
            with urllib.request.urlopen(req, timeout=5) as resp:
                return 200 <= resp.status < 300
        except Exception:
            return False

    def generate(self, prompt: str, *, system: Optional[str] = None, max_tokens: int = 256) -> Optional[str]:
        if not self.enabled:
            return None
        print(f"[Ollama] POST {self.base_url}/api/generate model={self.model}")
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.1,
                "num_predict": max_tokens,
            },
        }
        if system:
            payload["system"] = system

        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            self.base_url + "/api/generate",
            data=data,
            headers={"Content-Type": "application/json", "User-Agent": "Javis/1.0"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                raw = resp.read().decode("utf-8", errors="ignore")
            obj = json.loads(raw)
            text = self._clean_response(obj.get("response") or "")
            return text or None
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="ignore") if hasattr(exc, "read") else ""
            print(f"Ollama HTTP error: {exc.code} {body[:300]}")
        except Exception as exc:
            print(f"Ollama response error: {exc}")
        return None


ollama_client = OllamaClient()
