"""Permission guard between AI router and MCP/local tools."""

from typing import Any, Dict

from core.mcp.client import mcp_client
from core.security.tool_policy import get_tool_policy, get_legacy_policy


class PermissionGuard:
    def execute_tool_call(self, tool_call: Dict[str, Any]) -> Any:
        if not isinstance(tool_call, dict):
            return "Blocked: invalid tool call."

        tool_name = str(tool_call.get("tool", "")).strip()
        args = tool_call.get("args") or {}
        if not isinstance(args, dict):
            return "Blocked: invalid tool arguments."

        policy = get_tool_policy(tool_name)

        if policy == "blocked":
            reason = tool_call.get("reason") or "This tool is not allowed."
            return f"Blocked: {tool_name}. {reason}"

        if policy == "confirm":
            return (
                f"Confirmation required before running: {tool_name}. "
                f"Args: {args}. I will not execute it automatically."
            )

        return mcp_client.call_tool(tool_name, args)

    def check_legacy_function(self, function_name: str) -> str:
        return get_legacy_policy(function_name)

    def block_message(self, function_name: str) -> str:
        return f"Blocked: {function_name} is not allowed to send or delete data automatically."

    def confirm_message(self, function_name: str) -> str:
        return f"Confirmation required before running: {function_name}. I will not execute it automatically."


permission_guard = PermissionGuard()
