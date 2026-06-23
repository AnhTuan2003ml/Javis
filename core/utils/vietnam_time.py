"""Vietnam time helpers.

The project may run on machines/servers with a different local timezone.
Use these helpers whenever the assistant displays, stores, schedules or compares
local time so Javis behaves consistently for Vietnam users.
"""
from datetime import datetime, timezone, timedelta

try:
    from zoneinfo import ZoneInfo
except Exception:  # pragma: no cover - fallback for very old Python versions
    ZoneInfo = None

VIETNAM_TZ_NAME = "Asia/Ho_Chi_Minh"
VIETNAM_TZ = ZoneInfo(VIETNAM_TZ_NAME) if ZoneInfo else timezone(timedelta(hours=7), name="ICT")


def vn_now() -> datetime:
    """Return current Vietnam time as a naive datetime for legacy code compatibility."""
    return datetime.now(VIETNAM_TZ).replace(tzinfo=None)


def vn_fromtimestamp(timestamp: float) -> datetime:
    """Return a file/system timestamp converted to Vietnam time as a naive datetime."""
    return datetime.fromtimestamp(timestamp, VIETNAM_TZ).replace(tzinfo=None)


def vn_today_str(fmt: str = "%Y-%m-%d") -> str:
    """Return today's date/time in Vietnam formatted with strftime."""
    return vn_now().strftime(fmt)
