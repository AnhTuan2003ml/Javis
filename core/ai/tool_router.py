"""AI-first tool router for Javis.

The router returns JSON-like dicts. It does not execute anything.
Execution must go through PermissionGuard.
"""

from __future__ import annotations

import json
import re
from typing import Callable, Dict, Optional, Any


SYSTEM_PROMPT = """
You are Javis AI Tool Router.
Your job is to choose the best MCP tool for the user's command.
You can choose tools, but you cannot execute tools directly.
Never choose tools that delete data.
Never choose tools that send messages, emails, posts, or forms without explicit confirmation.
For dangerous actions, return tool "blocked" with a reason.
Return ONLY valid JSON.

Allowed safe tools:
1. answer_question(question: string) - answer/explain directly using the local AI model. Use this for questions like "what is AI", "explain AI", "AI là gì".
2. google_search(query: string) - search information on Google only when the user explicitly asks to search/google/look up on the web.
3. youtube_search(query: string) - search YouTube and show results.
4. youtube_play(query: string, index: number) - play/open the Nth video/song result on YouTube.
5. open_website(site: string) - open only the homepage of a website.
6. get_time() - get current time.

Return JSON format:
{"tool":"tool_name","args":{}}
""".strip()


class ToolRouter:
    def route(self, user_query: str, ai_generate: Optional[Callable[[str], str]] = None) -> Optional[Dict[str, Any]]:
        query = (user_query or "").strip()
        if not query:
            return None

        deterministic = self._route_deterministic(query)
        if deterministic:
            return deterministic

        if ai_generate:
            ai_result = self._route_with_ai(query, ai_generate)
            if ai_result:
                return ai_result

        return None

    def _route_deterministic(self, query: str) -> Optional[Dict[str, Any]]:
        q = query.lower().strip()
        q = re.sub(r"\s+", " ", q)

        # Hard blocked intents. Do not let the legacy command matcher execute them later.
        if re.search(r"\b(delete|remove|erase|x[oó]a|xoá|xóa)\b", q):
            return {"tool": "blocked", "args": {}, "reason": "Deleting data is not allowed from AI tool calls."}

        if re.search(r"\b(send|message|email|post|submit|gửi|gui)\b", q) and re.search(r"\b(to|cho|zalo|email|gmail|facebook|group|nhóm|nhom)\b", q):
            return {"tool": "blocked", "args": {}, "reason": "Sending or posting data is not allowed automatically."}


        # Follow-up after a YouTube search/play: "open the second video", "play second result".
        followup = re.search(r"^(?:open|play)?\s*(?:the\s+)?(first|second|third|fourth|fifth|1st|2nd|3rd|4th|5th|number\s+\d+|\d+)\s+(?:video|result)(?:\s+on\s+youtube)?$", q, re.IGNORECASE)
        if followup:
            index = self._ordinal_to_int(followup.group(1))
            return {"tool": "youtube_play", "args": {"query": "", "index": index}}

        # Example: "play billie jean the second video" or STT variant "billie jean to second video".
        embedded_ordinal = re.search(r"^(?:open|play)\s+(.+?)\s+(?:the|to)?\s*(first|second|third|fourth|fifth|1st|2nd|3rd|4th|5th|number\s+\d+|\d+)\s+(?:video|result)(?:\s+(?:in|on)\s+youtube)?$", q, re.IGNORECASE)
        if embedded_ordinal:
            term = self._clean_search_term(embedded_ordinal.group(1), provider="youtube")
            index = self._ordinal_to_int(embedded_ordinal.group(2))
            if term:
                return {"tool": "youtube_play", "args": {"query": term, "index": index}}

        # YouTube intent before generic website intent.
        # "play/open X in YouTube" should open the first video, while
        # "search X in YouTube" should only show search results.
        youtube_search_patterns = [
            r"^(?:search|find|look up)\s+(.+?)\s+(?:in|on)\s+youtube$",
            r"^(?:search|find|look up)\s+youtube\s+(?:for\s+)?(.+)$",
            r"^youtube\s+(?:search|find|look up)\s+(.+)$",
        ]
        for pattern in youtube_search_patterns:
            m = re.search(pattern, q, re.IGNORECASE)
            if m:
                term = self._clean_search_term(m.group(1), provider="youtube")
                if term:
                    return {"tool": "youtube_search", "args": {"query": term}}

        youtube_play_patterns = [
            r"^(?:open|play)\s+(.+?)\s+(?:in|on)\s+youtube$",
            r"^(?:open|play)\s+youtube\s+(?:for\s+)?(.+)$",
            r"^youtube\s+(?:play|open)\s+(.+)$",
            r"^(?:play)\s+(.+)$",
        ]
        for pattern in youtube_play_patterns:
            m = re.search(pattern, q, re.IGNORECASE)
            if m:
                term = self._clean_search_term(m.group(1), provider="youtube")
                if term and term not in {"youtube", "google"}:
                    return {"tool": "youtube_play", "args": {"query": term}}

        # Direct Q&A intent. Do this before Google intent so questions like
        # "what is AI" are answered by the local model instead of opening Google.
        if self._is_direct_question(q):
            return {"tool": "answer_question", "args": {"question": query.strip()}}

        # Google/search intent.
        google_patterns = [
            r"^(?:search|find|look up|google)\s+(?:for\s+)?(.+?)(?:\s+(?:on|in)\s+google)?$",
        ]
        for pattern in google_patterns:
            m = re.search(pattern, q, re.IGNORECASE)
            if m:
                term = self._clean_search_term(m.group(1), provider="google")
                if term and term not in {"google", "youtube"}:
                    return {"tool": "google_search", "args": {"query": term}}

        # Open only website homepage. Never route filler words such as "the" to Windows/open_app.
        m = re.search(r"^(?:open|go to|visit)\s+([a-z0-9_.-]+)(?:\s+website)?$", q, re.IGNORECASE)
        if m:
            site = m.group(1).strip()
            if site in {"the", "a", "an", "to", "for", "in", "on", "video", "result", "first", "second", "third"}:
                return {"tool": "blocked", "args": {}, "reason": f"'{site}' is not a valid app or website name."}
            if site in {"google", "youtube", "facebook", "github", "gmail", "wikipedia", "stackoverflow", "linkedin", "instagram", "twitter", "x"} or "." in site:
                return {"tool": "open_website", "args": {"site": site}}

        if q in {"what time is it", "time", "current time", "tell me the time", "time now", "what is time now"}:
            return {"tool": "get_time", "args": {}}

        return None

    def _route_with_ai(self, query: str, ai_generate: Callable[[str], str]) -> Optional[Dict[str, Any]]:
        prompt = f'{SYSTEM_PROMPT}\n\nUser command: "{query}"\nJSON:'
        try:
            raw = ai_generate(prompt)
            data = self._extract_json(raw)
            if not data:
                return None
            tool = data.get("tool")
            args = data.get("args", {})
            if not isinstance(tool, str) or not isinstance(args, dict):
                return None
            # Only allow known tool names out of AI router.
            if tool not in {"answer_question", "google_search", "youtube_search", "youtube_play", "open_website", "get_time", "blocked"}:
                return None
            if tool == "answer_question" and not args.get("question"):
                args["question"] = query
                data["args"] = args
            return data
        except Exception as exc:
            print(f"Tool router AI failed: {exc}")
            return None

    def _extract_json(self, raw: str) -> Optional[Dict[str, Any]]:
        if not raw:
            return None
        raw = raw.strip()
        try:
            return json.loads(raw)
        except Exception:
            pass
        m = re.search(r"\{.*\}", raw, flags=re.DOTALL)
        if not m:
            return None
        try:
            return json.loads(m.group(0))
        except Exception:
            return None

    def _is_direct_question(self, q: str) -> bool:
        q = (q or "").strip().lower()
        if not q:
            return False

        # Explicit web/search/open commands should stay tool actions.
        if re.search(r"\b(search|google|look up|find on google|open|play|youtube|website)\b", q):
            return False

        # Ignore incomplete accidental STT fragments such as "what is a".
        if q in {"what is a", "what is an", "what is the", "what is", "who is", "why", "how"}:
            return True

        question_starters = (
            "what is ", "what's ", "what are ", "who is ", "who's ", "who are ", "where is ", "where's ", "where are ",
            "when is ", "when are ", "why ", "how ", "explain ", "define ",
            "tell me about ", "can you explain ", "ai là gì", "là gì", "giải thích ",
            "giai thich ", "định nghĩa ", "dinh nghia "
        )
        if q.startswith(question_starters):
            return True

        # Vietnamese pattern: "X là gì" / "X la gi"
        if re.search(r"\b(là gì|la gi)\??$", q):
            return True

        return False

    def _ordinal_to_int(self, text: str) -> int:
        text = (text or "").lower().strip()
        mapping = {
            "first": 1, "1st": 1,
            "second": 2, "2nd": 2,
            "third": 3, "3rd": 3,
            "fourth": 4, "4th": 4,
            "fifth": 5, "5th": 5,
        }
        if text in mapping:
            return mapping[text]
        m = re.search(r"\d+", text)
        if m:
            return max(1, min(int(m.group(0)), 10))
        return 1

    def _clean_search_term(self, text: str, provider: str) -> str:
        text = (text or "").strip().lower()
        text = re.sub(r"\b(?:in|on)\s+youtube\b", "", text, flags=re.IGNORECASE)
        text = re.sub(r"\b(?:in|on)\s+google\b", "", text, flags=re.IGNORECASE)
        text = re.sub(r"\b(?:search|find|look up|open|play|for)\b", " ", text, flags=re.IGNORECASE)
        text = re.sub(r"\s+", " ", text).strip(" .,'\"")
        return text


tool_router = ToolRouter()
