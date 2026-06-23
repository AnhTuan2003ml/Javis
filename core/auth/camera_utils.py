"""Camera helpers for Javis Face Auth.

V6 fixes wrong-camera/black-camera selection:
- A frame is valid only when BOTH brightness and contrast are high enough.
- DSHOW black frames like brightness=0.09 are never accepted.
- The configured MSMF camera is tried first, but if it cannot grab a real frame,
  probing continues through MSMF/DSHOW/ANY and all camera indexes.
- Working camera settings are saved to config/camera_config.json.
"""

from __future__ import annotations

import json
import os
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Important Windows workaround. Must be set before cv2 is imported.
os.environ.setdefault("OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS", "0")
os.environ.setdefault("OPENCV_LOG_LEVEL", "ERROR")

import cv2
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[2]
CAMERA_CONFIG_PATH = PROJECT_ROOT / "config" / "camera_config.json"

BACKEND_MAP = {
    "MSMF": cv2.CAP_MSMF,
    "DSHOW": cv2.CAP_DSHOW,
    "ANY": cv2.CAP_ANY,
    "DEFAULT": cv2.CAP_ANY,
}


def _parse_int(value: object, default: Optional[int] = None) -> Optional[int]:
    try:
        if value is None:
            return default
        return int(str(value).strip())
    except Exception:
        return default


def _parse_float(value: object, default: float) -> float:
    try:
        if value is None:
            return default
        return float(str(value).strip())
    except Exception:
        return default


def _load_camera_config() -> Dict[str, object]:
    default = {
        "camera_index": 0,
        "camera_backend": "MSMF",
        "prefer_saved_camera": True,
        "auto_save_working_camera": True,
        "direct_open_for_auth": False,
        "max_index": 5,
        "width": 640,
        "height": 480,
        "read_timeout_seconds": 6.0,
        "warmup_frames": 20,
        "min_brightness": 15.0,
        "min_contrast": 8.0,
        "reject_dark_frame": True,
    }
    try:
        if CAMERA_CONFIG_PATH.exists():
            with CAMERA_CONFIG_PATH.open("r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, dict):
                default.update(data)
    except Exception as e:
        print(f"[Camera] Cannot read camera config: {e}", flush=True)
    return default


def _save_camera_config(info: Dict[str, object]) -> None:
    try:
        CAMERA_CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
        current = _load_camera_config()
        current.update(
            {
                "camera_index": int(info.get("index", 0)),
                "camera_backend": str(info.get("backend_name", "MSMF")).upper(),
                "prefer_saved_camera": True,
                "auto_save_working_camera": True,
                "direct_open_for_auth": False,
                "last_brightness": info.get("brightness"),
                "last_contrast": info.get("contrast"),
                "last_width": info.get("width"),
                "last_height": info.get("height"),
            }
        )
        with CAMERA_CONFIG_PATH.open("w", encoding="utf-8") as f:
            json.dump(current, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"[Camera] Cannot save camera config: {e}", flush=True)


def _backend_options() -> List[Tuple[str, int]]:
    return [("MSMF", cv2.CAP_MSMF), ("DSHOW", cv2.CAP_DSHOW), ("ANY", cv2.CAP_ANY)]


def _ordered_indices(max_index: int, config: Dict[str, object]) -> List[int]:
    env_index = os.getenv("JARVIS_CAMERA_INDEX", "").strip()
    indices = list(range(max_index + 1))
    selected: Optional[int] = None

    if env_index:
        selected = _parse_int(env_index)
    elif bool(config.get("prefer_saved_camera", True)):
        selected = _parse_int(config.get("camera_index"), 0)

    if selected is not None:
        if selected in indices:
            return [selected] + [i for i in indices if i != selected]
        return [selected] + indices
    return indices


def _filtered_backends(config: Dict[str, object]) -> List[Tuple[str, int]]:
    options = _backend_options()
    env_backend = os.getenv("JARVIS_CAMERA_BACKEND", "").strip().upper()
    selected = env_backend
    if not selected and bool(config.get("prefer_saved_camera", True)):
        selected = str(config.get("camera_backend", "MSMF")).strip().upper()
    if selected:
        filtered = [item for item in options if item[0] == selected]
        if filtered:
            return filtered + [item for item in options if item[0] != selected]
    return options


def frame_stats(frame: np.ndarray) -> Tuple[float, float]:
    if frame is None:
        return 0.0, 0.0
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) if len(frame.shape) == 3 else frame
    return float(gray.mean()), float(gray.std())


def is_black_frame(frame: np.ndarray, min_brightness: Optional[float] = None, min_contrast: Optional[float] = None) -> bool:
    """Return True for frames that are too dark/flat to be a real camera image.

    V5 used `brightness < min AND contrast < min`, which allowed almost black
    DSHOW frames through when contrast was slightly above 3. V6 uses OR.
    Example rejected: brightness=0.09, contrast=3.52.
    """
    config = _load_camera_config()
    if min_brightness is None:
        min_brightness = _parse_float(config.get("min_brightness"), 15.0)
    if min_contrast is None:
        min_contrast = _parse_float(config.get("min_contrast"), 8.0)
    brightness, contrast = frame_stats(frame)
    return brightness < min_brightness or contrast < min_contrast


def _configure_camera(cam: cv2.VideoCapture, width: int, height: int, backend_name: str = "") -> None:
    backend_name = (backend_name or "").upper()

    if backend_name == "DSHOW":
        # DSHOW often needs explicit pixel formats. Try YUY2 first, then MJPG.
        for fourcc in ("YUY2", "MJPG"):
            try:
                cam.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*fourcc))
            except Exception:
                pass

    cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    try:
        cam.set(cv2.CAP_PROP_FPS, 30)
    except Exception:
        pass
    try:
        cam.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    except Exception:
        pass


def _read_stable_frame(
    cam: cv2.VideoCapture,
    warmup_frames: int = 20,
    timeout_seconds: float = 6.0,
) -> Tuple[bool, Optional[np.ndarray]]:
    """Read a usable frame. Some Windows cameras open but fail on read."""
    frame = None
    ret = False
    deadline = time.time() + max(1.0, float(timeout_seconds))
    attempts = 0
    min_attempts = max(1, warmup_frames)

    while time.time() < deadline or attempts < min_attempts:
        attempts += 1
        try:
            ret, frame = cam.read()
        except Exception:
            ret, frame = False, None
        if ret and frame is not None:
            # Return the first readable frame. Validation is done by caller.
            return True, frame
        time.sleep(0.08)
        if attempts >= min_attempts and time.time() >= deadline:
            break

    return False, frame


def get_preferred_camera_settings() -> Tuple[int, str, int, int, int]:
    config = _load_camera_config()
    index = _parse_int(os.getenv("JARVIS_CAMERA_INDEX"), None)
    if index is None:
        index = _parse_int(config.get("camera_index"), 0) or 0

    backend_name = os.getenv("JARVIS_CAMERA_BACKEND", "").strip().upper()
    if not backend_name:
        backend_name = str(config.get("camera_backend", "MSMF")).strip().upper()
    if backend_name not in BACKEND_MAP:
        backend_name = "MSMF"

    width = _parse_int(config.get("width"), 640) or 640
    height = _parse_int(config.get("height"), 480) or 480
    max_index = _parse_int(config.get("max_index"), 5) or 5
    return index, backend_name, width, height, max_index


def open_preferred_camera_fast(validate: bool = True) -> Tuple[cv2.VideoCapture, Dict[str, object]]:
    index, backend_name, width, height, _ = get_preferred_camera_settings()
    backend = BACKEND_MAP.get(backend_name, cv2.CAP_MSMF)
    config = _load_camera_config()
    read_timeout = _parse_float(config.get("read_timeout_seconds"), 6.0)
    warmup = _parse_int(config.get("warmup_frames"), 20) or 20
    reject_dark = bool(config.get("reject_dark_frame", True))

    print(f"[Camera] Direct open: index={index}, backend={backend_name}", flush=True)
    cam = cv2.VideoCapture(index, backend)
    if not cam.isOpened():
        cam.release()
        raise RuntimeError(f"Cannot open configured camera index={index}, backend={backend_name}")

    _configure_camera(cam, width, height, backend_name)

    brightness = None
    contrast = None
    if validate:
        ret, frame = _read_stable_frame(cam, warmup_frames=warmup, timeout_seconds=read_timeout)
        if not ret or frame is None:
            cam.release()
            raise RuntimeError(f"Configured camera opened but cannot grab frame: index={index}, backend={backend_name}")
        brightness, contrast = frame_stats(frame)
        if reject_dark and is_black_frame(frame):
            cam.release()
            raise RuntimeError(
                f"Configured camera returns dark/black frame: index={index}, backend={backend_name}, "
                f"brightness={brightness:.2f}, contrast={contrast:.2f}"
            )

    info = {
        "index": index,
        "backend_name": backend_name,
        "backend": backend,
        "brightness": None if brightness is None else round(brightness, 2),
        "contrast": None if contrast is None else round(contrast, 2),
        "width": int(cam.get(cv2.CAP_PROP_FRAME_WIDTH)),
        "height": int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT)),
    }
    return cam, info


def open_working_camera(
    width: int = 640,
    height: int = 480,
    max_index: int = 5,
    warmup_frames: int = 20,
    allow_dark_fallback: bool = False,
) -> Tuple[cv2.VideoCapture, Dict[str, object]]:
    config = _load_camera_config()
    max_index = _parse_int(config.get("max_index"), max_index) or max_index
    width = _parse_int(config.get("width"), width) or width
    height = _parse_int(config.get("height"), height) or height
    read_timeout = _parse_float(config.get("read_timeout_seconds"), 6.0)
    warmup_frames = _parse_int(config.get("warmup_frames"), warmup_frames) or warmup_frames
    reject_dark = bool(config.get("reject_dark_frame", True))
    first_dark_info: Optional[Dict[str, object]] = None

    print(
        f"[Camera] Preferred camera: index={config.get('camera_index', 0)}, "
        f"backend={config.get('camera_backend', 'MSMF')}",
        flush=True,
    )

    for index in _ordered_indices(max_index, config):
        for backend_name, backend in _filtered_backends(config):
            print(f"[Camera] Trying index={index}, backend={backend_name}...", flush=True)
            cam = cv2.VideoCapture(index, backend)
            if not cam.isOpened():
                cam.release()
                print(f"[Camera] index={index}, backend={backend_name}: cannot open", flush=True)
                continue

            _configure_camera(cam, width, height, backend_name)
            ret, frame = _read_stable_frame(cam, warmup_frames=warmup_frames, timeout_seconds=read_timeout)
            if not ret or frame is None:
                cam.release()
                print(f"[Camera] index={index}, backend={backend_name}: cannot grab/read frame", flush=True)
                continue

            brightness, contrast = frame_stats(frame)
            info = {
                "index": index,
                "backend_name": backend_name,
                "backend": backend,
                "brightness": round(brightness, 2),
                "contrast": round(contrast, 2),
                "width": int(cam.get(cv2.CAP_PROP_FRAME_WIDTH)),
                "height": int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT)),
            }
            print(
                f"[Camera] index={index}, backend={backend_name}: "
                f"brightness={brightness:.2f}, contrast={contrast:.2f}",
                flush=True,
            )

            if reject_dark and is_black_frame(frame):
                if first_dark_info is None:
                    first_dark_info = info
                cam.release()
                print(
                    f"[Camera] index={index}, backend={backend_name}: rejected dark/black frame, trying next...",
                    flush=True,
                )
                continue

            print(f"[Camera] Using index={index}, backend={backend_name}", flush=True)
            if bool(config.get("auto_save_working_camera", True)):
                _save_camera_config(info)
            return cam, info

    if allow_dark_fallback and first_dark_info is not None:
        index = int(first_dark_info["index"])
        backend_name = str(first_dark_info["backend_name"])
        backend = int(first_dark_info["backend"])
        print(f"[Camera] WARNING: fallback to dark camera index={index}, backend={backend_name}", flush=True)
        cam = cv2.VideoCapture(index, backend)
        _configure_camera(cam, width, height, backend_name)
        return cam, first_dark_info

    raise RuntimeError(
        "No working camera found. The opened cameras were unreadable or too dark. "
        "Close all camera apps, then test with: python .\\core\\auth\\sample.py"
    )
