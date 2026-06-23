"""Global interrupt/cancel state for Jarvis.

This module is intentionally tiny and dependency-free so UI, command router,
TTS, and tools can all check the same cancel flag.
"""
import threading
from datetime import datetime

_interrupt_event = threading.Event()
_state_lock = threading.Lock()
_state = {
    "interrupted": False,
    "reason": "",
    "current_task": "idle",
    "updated_at": None,
}

CANCEL_PHRASES = {
    "cancel", "stop", "stop jarvis", "jarvis stop", "abort", "interrupt",
    "huy", "hủy", "dung", "dừng", "ngat", "ngắt", "ngắt lời", "hủy lệnh",
    "cancel command", "stop speaking", "shut up", "im lang", "im lặng",
}


def _now():
    return datetime.now().isoformat(timespec="seconds")


def request_interrupt(reason="user_requested"):
    """Signal all cooperative Jarvis tasks to stop as soon as possible."""
    _interrupt_event.set()
    with _state_lock:
        _state.update({
            "interrupted": True,
            "reason": str(reason or "user_requested"),
            "updated_at": _now(),
        })
    # Best-effort stop for pygame/gTTS playback.
    try:
        import pygame
        if pygame.mixer.get_init():
            pygame.mixer.music.stop()
    except Exception:
        pass
    return True


def clear_interrupt():
    """Clear cancel flag before starting a new user command."""
    _interrupt_event.clear()
    with _state_lock:
        _state.update({
            "interrupted": False,
            "reason": "",
            "updated_at": _now(),
        })


def is_interrupted():
    return _interrupt_event.is_set()


def should_cancel_command(text):
    normalized = str(text or "").strip().lower()
    return normalized in CANCEL_PHRASES


def set_current_task(task):
    with _state_lock:
        _state["current_task"] = str(task or "idle")
        _state["updated_at"] = _now()


def get_state():
    with _state_lock:
        return dict(_state)
