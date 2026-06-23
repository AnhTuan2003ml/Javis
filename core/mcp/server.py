"""Optional MCP server for Javis tools.

Install optional package first:
    pip install mcp
Run:
    python -m core.mcp.server

The app also has a local MCP-style client fallback, so Javis can work without
this optional server during development.
"""

try:
    from mcp.server.fastmcp import FastMCP
except Exception as exc:  # pragma: no cover
    FastMCP = None
    MCP_IMPORT_ERROR = exc

from core.tools.browser_tools import google_search, youtube_search, youtube_play, open_website
from core.utils.vietnam_time import vn_now
from core.ai.ollama_client import ollama_client


if FastMCP:
    mcp = FastMCP("javis-safe-tools")

    @mcp.tool()
    def google_search_tool(query: str) -> str:
        """Search information on Google. Read/open only, no posting or sending."""
        return google_search(query)

    @mcp.tool()
    def youtube_search_tool(query: str) -> str:
        """Search videos or songs on YouTube. Read/open only."""
        return youtube_search(query)

    @mcp.tool()
    def youtube_play_tool(query: str, index: int = 1) -> str:
        """Open the Nth YouTube video/song result. Read/open only."""
        return youtube_play(query, index=index)

    @mcp.tool()
    def open_website_tool(site: str) -> str:
        """Open a website homepage. Read/open only."""
        return open_website(site)

    @mcp.tool()
    def get_time_tool() -> str:
        """Get current Vietnam time."""
        return vn_now().strftime("%I:%M %p")

    @mcp.tool()
    def answer_question_tool(question: str) -> str:
        """Answer a direct user question using the configured local Ollama model."""
        system = (
            "You are Javis, a concise voice assistant. Answer directly and briefly. "
            "If the user asks in Vietnamese, answer in Vietnamese; otherwise answer in English."
        )
        answer = ollama_client.generate(
            f"Question: {question}\n\nAnswer briefly:",
            system=system,
            max_tokens=220,
        )
        return answer or "I'm having trouble answering that with the local model."


def main():
    if not FastMCP:
        raise RuntimeError(f"Optional MCP package is not installed: {MCP_IMPORT_ERROR}")
    mcp.run()


if __name__ == "__main__":
    main()
