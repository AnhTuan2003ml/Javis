"""Javis MCP client facade.

For now this exposes a local MCP-style call_tool(name, args) interface so the
rest of the app can use MCP semantics even when the optional `mcp` package is
not installed. Later you can replace call_tool() with a real MCP session call.
"""

from typing import Any, Dict

from core.tools.browser_tools import google_search, youtube_search, youtube_play, open_website
from core.utils.vietnam_time import vn_now
from core.ai.ollama_client import ollama_client


class LocalMCPClient:
    def __init__(self):
        self.tools = {
            "google_search": google_search,
            "youtube_search": youtube_search,
            "youtube_play": youtube_play,
            "open_website": open_website,
            "get_time": lambda: vn_now().strftime("%I:%M %p"),
            "answer_question": self.answer_question,
        }

    def answer_question(self, question: str) -> str:
        question = (question or "").strip()
        if not question:
            return "I didn't hear a complete question."

        # Avoid wasting the local model on tiny/incomplete STT fragments.
        if question.lower() in {"what is a", "what is an", "what is the", "what is"}:
            return "I heard an incomplete question. Please say the full topic."

        system = (
            "You are Javis, a concise voice assistant. "
            "Answer the user's question directly. "
            "Do not say you are searching the web. "
            "Do not include reasoning, analysis, or <think> tags. "
            "Keep the answer short, clear, and useful for voice output. "
            "If the user asks in Vietnamese, answer in Vietnamese; otherwise answer in English."
        )
        prompt = f"Question: {question}\n\nFinal answer only, briefly:"
        answer = ollama_client.generate(prompt, system=system, max_tokens=120)
        if answer:
            return answer.strip()
        return "I'm having trouble answering that with the local model."

    def call_tool(self, name: str, args: Dict[str, Any] | None = None) -> Any:
        args = args or {}
        if name not in self.tools:
            raise ValueError(f"MCP tool not found: {name}")
        return self.tools[name](**args)


mcp_client = LocalMCPClient()
