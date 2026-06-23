"""Central permission policy for Javis tool calls."""

SAFE_TOOLS = {
    "answer_question",
    "google_search",
    "youtube_search",
    "youtube_play",
    "open_website",
    "get_time",
}

CONFIRM_TOOLS = {
    "send_message",
    "send_email",
    "post_message",
    "submit_form",
    "create_file",
    "edit_file",
    "move_file",
    "rename_file",
    "run_terminal_command",
    "install_package",
    "shutdown",
    "restart",
    "hibernate",
    "sleep",
}

# Hard block: AI/tool-call layer must never send or delete data directly.
BLOCKED_TOOLS = {
    "delete_file",
    "delete_folder",
    "delete_message",
    "delete_email",
    "delete_contact",
    "email_sender",
    "send_message_without_confirm",
    "send_email_without_confirm",
    "post_public_content",
    "transfer_money",
    "change_password",
    "logout_all_devices",
    "clean_temp",
    "file_organizer",  # can move/delete files unpredictably
}

# Existing function names in dual_ai/new_features that need protection.
LEGACY_BLOCKED_FUNCTIONS = set(BLOCKED_TOOLS) | {
    "email_sender",
    "auto_reply",
    "auto_reply_message",
}

LEGACY_CONFIRM_FUNCTIONS = set(CONFIRM_TOOLS) | {
    "create_new_file",
    "create_folder",
    "sort_files",
    "auto_backup",
    "schedule_shutdown",
    "manage_package",
    "docker_control",
    "file_vault_encrypt",
    "file_vault_decrypt",
}


def get_tool_policy(tool_name: str) -> str:
    name = (tool_name or "").strip()
    if name in BLOCKED_TOOLS:
        return "blocked"
    if name in CONFIRM_TOOLS:
        return "confirm"
    if name in SAFE_TOOLS:
        return "safe"
    # Unknown MCP tools default to blocked, not safe.
    return "blocked"


def get_legacy_policy(function_name: str) -> str:
    name = (function_name or "").strip()
    if name in LEGACY_BLOCKED_FUNCTIONS:
        return "blocked"
    if name in LEGACY_CONFIRM_FUNCTIONS:
        return "confirm"
    return "safe"
